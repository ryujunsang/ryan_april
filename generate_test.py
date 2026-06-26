#!/usr/bin/env python3
"""
generate_test.py <prefix>

이미지 파일(예: L5_no1.jpg, L5_no2.jpg ...)을 읽어
Claude API로 문제를 추출하고 인터랙티브 HTML 시험지를 생성합니다.

사용법:
  python generate_test.py L5
  python generate_test.py L5 --model claude-opus-4-8   # 모델 변경
"""

import sys, os, base64, json, glob, re, argparse
import anthropic

EXTRACT_PROMPT = """이 영어 시험지 이미지들을 분석하여 JSON만 출력하세요 (설명 없이).

출력 형식:
{
  "lesson": "Lesson 4",
  "topic": "Architectural Acoustics",
  "topic_kr": "건축 음향학",
  "sec1": [
    {"q": "absorbed", "a": "흡수된"},
    {"q": "강도 (세기)", "a": "intensity", "note": "영어로"}
  ],
  "sec2": [
    {"q": "달갑지 않는", "a": ["undesirable"]}
  ],
  "sec3": [
    {
      "kr": "잔향을 조절하다",
      "parts": [
        {"b": true, "a": ["control"], "sz": 9},
        {"t": " reverberation."}
      ]
    }
  ],
  "sec4": [
    {
      "kr": "콘서트홀은 건축음향학을 이용하여 청중의 청취체험을 극대화한다.",
      "parts": [
        {"t": "Concert halls use "},
        {"b": true, "a": ["architectural"], "sz": 14},
        {"t": " "},
        {"b": true, "a": ["acoustics"], "sz": 10},
        {"t": " to maximize the audience's "},
        {"b": true, "a": ["listening"], "sz": 10},
        {"t": " experience."}
      ]
    }
  ]
}

섹션 규칙:
- sec1 (一) 단어 뜻 쓰기: q=주어진 단어(또는 한국어), a=정답. 한국어→영어이면 note:"영어로" 추가.
- sec2 (二) 우리말→영어: q=한국어, a=허용 영어 정답 배열(동의어 포함).
- sec3 (三) Collocation/빈칸: 영어 문장을 고정텍스트(t)와 빈칸(b:true)으로 분리. a=정답 배열, sz=입력 너비(글자수+3).
- sec4 (四) 문장 완성: sec3과 동일 형식. kr=한국어 해석.
- 존재하지 않는 섹션은 빈 배열 [].
- JSON 외 텍스트 출력 금지.
"""


def img_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode()


def extract_data(prefix: str, model: str) -> dict:
    client = anthropic.Anthropic()
    patterns = [f"{prefix}_no*.jpg", f"{prefix}_no*.jpeg", f"{prefix}_no*.png"]
    paths = []
    for pat in patterns:
        paths.extend(glob.glob(pat))
    paths = sorted(set(paths))

    if not paths:
        print(f"[ERROR] 이미지 없음: {prefix}_no*.jpg")
        sys.exit(1)

    print(f"[INFO] 이미지: {paths}")
    content = []
    for p in paths:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": img_b64(p),
            },
        })
    content.append({"type": "text", "text": EXTRACT_PROMPT})

    print(f"[INFO] Claude API 호출 중 ({model})...")
    resp = client.messages.create(
        model=model,
        max_tokens=8096,
        messages=[{"role": "user", "content": content}],
    )
    text = resp.content[0].text.strip()
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        print(f"[ERROR] JSON 파싱 실패:\n{text}")
        sys.exit(1)
    data = json.loads(m.group())
    for key in ("sec1", "sec2", "sec3", "sec4"):
        data.setdefault(key, [])
    print(f"[INFO] 추출 완료 — sec1:{len(data['sec1'])}개  sec2:{len(data['sec2'])}개  "
          f"sec3:{len(data['sec3'])}개  sec4:{len(data['sec4'])}개")
    return data


# ─── HTML 템플릿 ─────────────────────────────────────────────────────────────
# «LESSON»  «TOPIC_KR»  «TOPIC»  «S1»  «S2»  «S3»  «S4» 를 치환합니다.
HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>«LESSON» Test</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body {
  font-family: 'Segoe UI', Arial, sans-serif;
  background: linear-gradient(135deg, #eef2ff 0%, #e8f4fd 100%);
  min-height: 100vh; padding-bottom: 40px;
}
#header {
  background: linear-gradient(135deg, #1a2860, #2574a9);
  color: white; padding: 14px 20px 12px;
  text-align: center; position: sticky; top: 0; z-index: 20;
  box-shadow: 0 2px 10px rgba(37,116,169,0.4);
}
#header h1 { font-size: 18px; font-weight: bold; letter-spacing: 0.3px; }
#header p  { font-size: 11px; opacity: 0.75; margin-top: 3px; }
#tabs {
  display: flex; background: white; border-bottom: 2px solid #c5d0f0;
  overflow-x: auto; position: sticky; top: 56px; z-index: 10;
  -ms-overflow-style: none; scrollbar-width: none;
}
#tabs::-webkit-scrollbar { display: none; }
.tab {
  padding: 10px 14px; font-size: 13px; font-weight: bold; color: #889;
  cursor: pointer; border-bottom: 3px solid transparent;
  white-space: nowrap; flex-shrink: 0; transition: all 0.2s;
  -webkit-tap-highlight-color: transparent;
}
.tab.active { color: #2574a9; border-bottom-color: #2574a9; }
.section { display: none; padding: 16px; max-width: 680px; margin: 0 auto; }
.section.active { display: block; }
.sec-hd { font-size: 15px; font-weight: bold; color: #1a2860; margin-bottom: 3px; }
.sec-sub { font-size: 12px; color: #667; margin-bottom: 14px; }
.q-row {
  display: flex; align-items: center; gap: 8px;
  background: white; border: 1.5px solid #c5d0f0; border-radius: 9px;
  padding: 9px 12px; margin-bottom: 8px; transition: border-color 0.2s, background 0.2s;
}
.q-row.correct { border-color: #1e8449; background: #f4fff7; }
.q-row.wrong   { border-color: #c0392b; background: #fff4f4; }
.q-num  { font-size: 12px; font-weight: bold; color: #2574a9; min-width: 22px; flex-shrink: 0; }
.q-word { font-size: 14px; color: #1a2860; font-weight: 500; min-width: 140px; flex-shrink: 0; line-height: 1.4; }
.q-word.kr { color: #8e44ad; }
.q-input {
  flex: 1; border: 1.5px solid #c5d0f0; border-radius: 6px;
  padding: 6px 9px; font-size: 14px; outline: none; background: #f8f9ff; min-width: 0;
  transition: border-color 0.2s;
}
.q-input:focus { border-color: #2574a9; background: white; }
.q-ans { font-size: 12px; color: #1e8449; font-weight: bold; display: none; flex-shrink: 0; max-width: 130px; }
.sent-item {
  background: white; border: 1.5px solid #c5d0f0; border-radius: 10px;
  padding: 13px 14px; margin-bottom: 12px;
}
.sent-num { font-size: 12px; font-weight: bold; color: #2574a9; margin-bottom: 4px; }
.sent-kr  { font-size: 13px; color: #556; margin-bottom: 9px; line-height: 1.55; }
.sent-en  { font-size: 14px; color: #1a2860; line-height: 2.5; word-break: keep-all; }
.blank {
  display: inline-block; border: none; border-bottom: 2px solid #2574a9;
  background: transparent; font-size: 14px; color: #1a2860; outline: none;
  padding: 0 3px; text-align: center; vertical-align: bottom;
  transition: border-color 0.2s, color 0.2s;
}
.blank:focus  { border-bottom-color: #8e44ad; }
.blank.correct{ border-bottom-color: #1e8449; color: #1e8449; }
.blank.wrong  { border-bottom-color: #c0392b; color: #c0392b; }
.btn-row { display: flex; gap: 10px; margin: 18px 0 8px; flex-wrap: wrap; }
.btn {
  padding: 10px 20px; border: none; border-radius: 8px;
  font-size: 14px; font-weight: bold; color: white; cursor: pointer;
  transition: opacity 0.15s; -webkit-tap-highlight-color: transparent;
}
.btn:active { opacity: 0.75; }
.btn-blue   { background: #2574a9; }
.btn-purple { background: #8e44ad; }
.btn-gray   { background: #7f8c8d; }
.result-box {
  background: #f0f8ff; border: 1.5px solid #2574a9; border-radius: 9px;
  padding: 11px 14px; font-size: 14px; color: #1a2860; display: none; margin-top: 6px;
}
.result-box.show { display: block; }
.note-tag {
  font-size: 10px; color: #e67e22; background: #fff3e0;
  border-radius: 3px; padding: 1px 4px; margin-left: 4px;
}
.empty-notice {
  text-align: center; color: #aab; font-size: 14px; padding: 40px 0;
}
</style>
</head>
<body>

<div id="header">
  <h1>&#x1F4DD; ENGLISH Test &#x2014; «LESSON»</h1>
  <p>«TOPIC_KR» («TOPIC»)</p>
</div>

<div id="tabs">
  <div class="tab active"  onclick="showTab(0)">(&#x4E00;) &#xB2E8;&#xC5B4; &#xB73B;</div>
  <div class="tab"         onclick="showTab(1)">(&#x4E8C;) &#xC6B0;&#xB9AC;&#xB9D0;&#x2192;&#xC601;&#xC5B4;</div>
  <div class="tab"         onclick="showTab(2)">(&#x4E09;) Collocation</div>
  <div class="tab"         onclick="showTab(3)">(&#x56DB;) &#xBB38;&#xC7A5; &#xC644;&#xC131;</div>
</div>

<div class="section active" id="sec0">
  <div class="sec-hd">(&#x4E00;) &#xB2E4;&#xC74C; &#xB2E8;&#xC5B4;&#xC758; &#xB73B;&#xC744; &#xC4F0;&#xC138;&#xC694;.</div>
  <div class="sec-sub">&#xB2E8;&#xC5B4;&#xB97C; &#xBCF4;&#xACE0; &#xB73B;&#xC744; &#xC4F0;&#xC138;&#xC694;.</div>
  <div id="s1-wrap"></div>
  <div class="btn-row">
    <button class="btn btn-purple" onclick="showSec1()">&#xC815;&#xB2F5; &#xBCF4;&#xAE30;</button>
    <button class="btn btn-gray"   onclick="resetSec1()">&#xCD08;&#xAE30;&#xD654;</button>
  </div>
</div>

<div class="section" id="sec1">
  <div class="sec-hd">(&#x4E8C;) &#xB2E4;&#xC74C; &#xC6B0;&#xB9AC;&#xB9D0;&#xC744; &#xC601;&#xC5B4;&#xB85C; &#xC4F0;&#xC138;&#xC694;.</div>
  <div class="sec-sub">&#xD55C;&#xAD6D;&#xC5B4;&#xB97C; &#xBCF4;&#xACE0; &#xC601;&#xC5B4; &#xB2E8;&#xC5B4;&#xB97C; &#xC785;&#xB825;&#xD558;&#xC138;&#xC694;.</div>
  <div id="s2-wrap"></div>
  <div class="btn-row">
    <button class="btn btn-blue" onclick="checkSec2()">&#xC815;&#xB2F5; &#xD655;&#xC778;</button>
    <button class="btn btn-gray" onclick="resetSec2()">&#xCD08;&#xAE30;&#xD654;</button>
  </div>
  <div class="result-box" id="s2-result"></div>
</div>

<div class="section" id="sec2">
  <div class="sec-hd">(&#x4E09;) &#xB2E4;&#xC74C; Collocation&#xC744; &#xC644;&#xC131;&#xD558;&#xC138;&#xC694;.</div>
  <div class="sec-sub">&#xC6B0;&#xB9AC;&#xB9D0;&#xC744; &#xCC38;&#xACE0;&#xD558;&#xC5EC; &#xBE48;&#xCE78;&#xC744; &#xCC44;&#xC6B0;&#xC138;&#xC694;.</div>
  <div id="s3-wrap"></div>
  <div class="btn-row">
    <button class="btn btn-blue" onclick="checkSec3()">&#xC815;&#xB2F5; &#xD655;&#xC778;</button>
    <button class="btn btn-gray" onclick="resetSec3()">&#xCD08;&#xAE30;&#xD654;</button>
  </div>
  <div class="result-box" id="s3-result"></div>
</div>

<div class="section" id="sec3">
  <div class="sec-hd">(&#x56DB;) &#xB2E4;&#xC74C; &#xC601;&#xC5B4; &#xBB38;&#xC7A5;&#xC744; &#xC644;&#xC131;&#xD558;&#xC138;&#xC694;.</div>
  <div class="sec-sub">&#xC6B0;&#xB9AC;&#xB9D0;&#xC744; &#xCC38;&#xACE0;&#xD558;&#xC5EC; &#xBE48;&#xCE78;&#xC744; &#xCC44;&#xC6B0;&#xC138;&#xC694;.</div>
  <div id="s4-wrap"></div>
  <div class="btn-row">
    <button class="btn btn-blue" onclick="checkSec4()">&#xC815;&#xB2F5; &#xD655;&#xC778;</button>
    <button class="btn btn-gray" onclick="resetSec4()">&#xCD08;&#xAE30;&#xD654;</button>
  </div>
  <div class="result-box" id="s4-result"></div>
</div>

<script>
function showTab(i) {
  document.querySelectorAll('.tab').forEach((t, j) => t.classList.toggle('active', i === j));
  document.querySelectorAll('.section').forEach((s, j) => s.classList.toggle('active', i === j));
}

const S1_DATA = «S1»;
const S2_DATA = «S2»;
const S3_DATA = «S3»;
const S4_DATA = «S4»;

/* ── Section 一 ── */
(function buildS1() {
  const wrap = document.getElementById('s1-wrap');
  if (!S1_DATA.length) { wrap.innerHTML = '<div class="empty-notice">문항 없음</div>'; return; }
  S1_DATA.forEach((item, i) => {
    const row = document.createElement('div');
    row.className = 'q-row';
    const isKr = !!item.note;
    row.innerHTML =
      '<span class="q-num">(' + (i+1) + ')</span>' +
      '<span class="q-word' + (isKr ? ' kr' : '') + '">' + item.q +
        (item.note ? '<span class="note-tag">' + item.note + '</span>' : '') + '</span>' +
      '<input class="q-input" type="text" id="s1-' + i + '" placeholder="정답...">' +
      '<span class="q-ans" id="s1a-' + i + '">' + item.a + '</span>';
    wrap.appendChild(row);
  });
})();

function showSec1() {
  S1_DATA.forEach((_, i) => { document.getElementById('s1a-' + i).style.display = 'inline'; });
}
function resetSec1() {
  S1_DATA.forEach((_, i) => {
    document.getElementById('s1-' + i).value = '';
    document.getElementById('s1a-' + i).style.display = 'none';
  });
}

/* ── Section 二 ── */
(function buildS2() {
  const wrap = document.getElementById('s2-wrap');
  if (!S2_DATA.length) { wrap.innerHTML = '<div class="empty-notice">문항 없음</div>'; return; }
  S2_DATA.forEach((item, i) => {
    const row = document.createElement('div');
    row.className = 'q-row'; row.id = 's2r-' + i;
    row.innerHTML =
      '<span class="q-num">(' + (i+1) + ')</span>' +
      '<span class="q-word kr">' + item.q + '</span>' +
      '<span style="color:#aab;flex-shrink:0">&rarr;</span>' +
      '<input class="q-input" type="text" id="s2-' + i + '" placeholder="영어로...">';
    wrap.appendChild(row);
  });
})();

function checkSec2() {
  let ok = 0;
  S2_DATA.forEach((item, i) => {
    const val = (document.getElementById('s2-' + i).value || '').trim().toLowerCase();
    const pass = item.a.some(a => val === a.toLowerCase());
    const row = document.getElementById('s2r-' + i);
    row.classList.toggle('correct', pass); row.classList.toggle('wrong', !pass && val !== '');
    if (pass) ok++;
  });
  showResult('s2-result', ok, S2_DATA.length);
}
function resetSec2() {
  S2_DATA.forEach((_, i) => {
    document.getElementById('s2-' + i).value = '';
    const r = document.getElementById('s2r-' + i);
    r.classList.remove('correct', 'wrong');
  });
  hideResult('s2-result');
}

/* ── Section 三 ── */
let s3Map = [];
(function buildS3() {
  const wrap = document.getElementById('s3-wrap');
  if (!S3_DATA.length) { wrap.innerHTML = '<div class="empty-notice">문항 없음</div>'; return; }
  let idx = 0; s3Map = [];
  S3_DATA.forEach((item, qi) => {
    const div = document.createElement('div'); div.className = 'sent-item';
    div.innerHTML = '<div class="sent-num">(' + (qi+1) + ')</div>' +
                    '<div class="sent-kr">' + item.kr + '</div>';
    const en = document.createElement('div'); en.className = 'sent-en';
    item.parts.forEach(p => {
      if (p.b) {
        const inp = document.createElement('input');
        inp.className = 'blank'; inp.type = 'text'; inp.size = p.sz || 10;
        inp.id = 's3b-' + idx; s3Map.push({idx, a: p.a}); idx++;
        en.appendChild(inp);
      } else { en.appendChild(document.createTextNode(p.t)); }
    });
    div.appendChild(en); wrap.appendChild(div);
  });
})();

function checkSec3() {
  let ok = 0;
  s3Map.forEach(({idx, a}) => {
    const el = document.getElementById('s3b-' + idx);
    const val = (el.value || '').trim().toLowerCase();
    const pass = a.some(x => val === x.toLowerCase());
    el.classList.toggle('correct', pass); el.classList.toggle('wrong', !pass && val !== '');
    if (pass) ok++;
  });
  showResult('s3-result', ok, s3Map.length);
}
function resetSec3() {
  s3Map.forEach(({idx}) => {
    const el = document.getElementById('s3b-' + idx); el.value = '';
    el.classList.remove('correct', 'wrong');
  });
  hideResult('s3-result');
}

/* ── Section 四 ── */
let s4Map = [];
(function buildS4() {
  const wrap = document.getElementById('s4-wrap');
  if (!S4_DATA.length) { wrap.innerHTML = '<div class="empty-notice">문항 없음</div>'; return; }
  let idx = 0; s4Map = [];
  S4_DATA.forEach((item, qi) => {
    const div = document.createElement('div'); div.className = 'sent-item';
    div.innerHTML = '<div class="sent-num">(' + (qi+1) + ')</div>' +
                    '<div class="sent-kr">' + item.kr + '</div>';
    const en = document.createElement('div'); en.className = 'sent-en';
    item.parts.forEach(p => {
      if (p.b) {
        const inp = document.createElement('input');
        inp.className = 'blank'; inp.type = 'text'; inp.size = p.sz || 10;
        inp.id = 's4b-' + idx; s4Map.push({idx, a: p.a}); idx++;
        en.appendChild(inp);
      } else { en.appendChild(document.createTextNode(p.t)); }
    });
    div.appendChild(en); wrap.appendChild(div);
  });
})();

function checkSec4() {
  let ok = 0;
  s4Map.forEach(({idx, a}) => {
    const el = document.getElementById('s4b-' + idx);
    const val = (el.value || '').trim().toLowerCase();
    const pass = a.some(x => val === x.toLowerCase());
    el.classList.toggle('correct', pass); el.classList.toggle('wrong', !pass && val !== '');
    if (pass) ok++;
  });
  showResult('s4-result', ok, s4Map.length);
}
function resetSec4() {
  s4Map.forEach(({idx}) => {
    const el = document.getElementById('s4b-' + idx); el.value = '';
    el.classList.remove('correct', 'wrong');
  });
  hideResult('s4-result');
}

/* ── Helpers ── */
function showResult(id, correct, total) {
  const el = document.getElementById(id);
  const pct = total ? Math.round(correct / total * 100) : 0;
  el.className = 'result-box show';
  el.innerHTML = '&#x2705; 정답: <strong>' + correct + ' / ' + total + '</strong>&nbsp;&nbsp;(' + pct + '%)' +
    (pct === 100 ? '&nbsp; &#x1F389; 완벽!' : pct >= 70 ? '&nbsp; &#x1F44D; 잘했어요!' : '&nbsp; &#x1F4AA; 다시 도전!');
}
function hideResult(id) { document.getElementById(id).className = 'result-box'; }

document.addEventListener('keydown', e => {
  if (e.key === 'Enter') {
    const inputs = Array.from(document.querySelectorAll('.section.active input'));
    const i = inputs.indexOf(document.activeElement);
    if (i >= 0 && i < inputs.length - 1) inputs[i + 1].focus();
  }
});
</script>
</body>
</html>
"""


def build_html(data: dict) -> str:
    s1 = json.dumps(data["sec1"], ensure_ascii=False)
    s2 = json.dumps(data["sec2"], ensure_ascii=False)
    s3 = json.dumps(data["sec3"], ensure_ascii=False)
    s4 = json.dumps(data["sec4"], ensure_ascii=False)
    html = HTML_TEMPLATE
    html = html.replace("«LESSON»",   data.get("lesson",   "Lesson"))
    html = html.replace("«TOPIC_KR»", data.get("topic_kr", ""))
    html = html.replace("«TOPIC»",    data.get("topic",    ""))
    html = html.replace("«S1»", s1).replace("«S2»", s2) \
               .replace("«S3»", s3).replace("«S4»", s4)
    return html


def main():
    parser = argparse.ArgumentParser(description="시험지 이미지 → HTML 생성")
    parser.add_argument("prefix", help="이미지 파일 접두어 (예: L5)")
    parser.add_argument("--model", default="claude-sonnet-4-6",
                        help="사용할 Claude 모델 (기본: claude-sonnet-4-6)")
    args = parser.parse_args()

    prefix = args.prefix.rstrip("_")
    data = extract_data(prefix, args.model)
    html = build_html(data)

    outfile = f"{prefix}_test.html"
    with open(outfile, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"[DONE] 생성 완료: {outfile}")


if __name__ == "__main__":
    main()
