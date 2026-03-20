
import json, base64, shutil, os

ui = {
    "title":"단어 계단 퀴즈","hint":"한국어 뜻 -> 영어 단어 입력:",
    "placeholder":"영어 단어를 입력하세요...",
    "btn_check":"정답 확인","btn_next":"다음 문제","btn_retry":"처음부터 다시",
    "correct":"정답!  ->  ","wrong":"오답!  정답: ",
    "empty":"먼저 단어를 입력하세요!",
    "stair":"현재 계단: ","score":"  |  정답: ","q_label":"문제  ",
    "win_title":"축하합니다!",
    "win_msg":"보물을 손에 넣었습니다!\n모든 계단을 올라 보물을 획득했어요!\n최종 정답: ",
    "end_title":"게임 종료",
    "end_msg":"아쉽게도 보물에 닿지 못했어요.\n정답: ",
    "end_msg2":" 문제\n다시 도전해 보세요!",
    "slide":"미끄러짐!  정답: ",
    "file_err":"vocab.json 파일을 찾을 수 없습니다.\n같은 폴더에 vocab.json 을 넣어주세요.",
    "file_err2":"vocab.json 읽기 오류: ",
    "retry_confirm":"처음부터 다시 시작할까요?",
    "retry_title":"재시작",
}
UB = base64.b64encode(json.dumps(ui, ensure_ascii=False).encode("utf-8")).decode("ascii")

vocab = [
    {"word": "brief",         "meaning": "adj. 간략한 (short)"},
    {"word": "renovation",    "meaning": "n. 수리 (redevelopment)"},
    {"word": "out-of-order",  "meaning": "adj. 사용할 수 없는"},
    {"word": "complete",      "meaning": "adj. 완료된 (accomplished)"},
    {"word": "inconvenience", "meaning": "n. 불편 (trouble)"},
    {"word": "vote",          "meaning": "v. 투표하다"},
    {"word": "detention",     "meaning": "n. 방과 후 남게 하기 (custody)"},
    {"word": "receive",       "meaning": "v. 얻다 (get)"},
    {"word": "peel off",      "meaning": "v. 껍질을 벗기다"},
    {"word": "rotten",        "meaning": "adj. 썩은 (decaying)"},
    {"word": "despite",       "meaning": "prep. ~에도 불구하고 (in spite of)"},
    {"word": "forbid",        "meaning": "v. 금하다 (prohibit, ban)"},
    {"word": "involve",       "meaning": "v. 포함하다"},
    {"word": "express",       "meaning": "v. 표현하다 (show)"},
    {"word": "intended for",  "meaning": "~를 위해서 만들어진, 계획된"},
    {"word": "deaf",          "meaning": "adj. 청각 장애가 있는"},
    {"word": "mute",          "meaning": "adj. 말을 못하는, 벙어리의"},
    {"word": "impressively",  "meaning": "adv. 인상 깊게"},
    {"word": "ape",           "meaning": "n. 유인원"},
    {"word": "vocal cords",   "meaning": "성대"},
    {"word": "companionship", "meaning": "n. 동료애 (friendship)"},
    {"word": "eventually",    "meaning": "adv. 마침내 (finally)"},
    {"word": "combine",       "meaning": "v. 결합하다 (put together)"},
    {"word": "now and then",  "meaning": "가끔 (sometimes)"},
    {"word": "waste",         "meaning": "n. 쓰레기, 낭비 (garbage, lavishness)"},
    {"word": "semester",      "meaning": "n. 학기"},
    {"word": "note",          "meaning": "n. 음표"},
    {"word": "scream",        "meaning": "v. 소리지르다 (shout)"},
    {"word": "latest",        "meaning": "adj. 최근의 (current)"},
    {"word": "wonder",        "meaning": "v. 궁금해하다 (question)"},
]

with open("output/vocab.json", "w", encoding="utf-8") as f:
    json.dump(vocab, f, ensure_ascii=False, indent=2)

print("UB ready, vocab.json saved")
print(UB)
