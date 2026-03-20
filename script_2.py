
# 박스 드로잉 문자 제거
py_final = py_final.replace('\u2500', '-')
bad = [(i,c) for i,c in enumerate(py_final) if ord(c)>127]
print("Non-ASCII after fix:", len(bad))

with open("output/vocab_stairs.py", "w", encoding="ascii") as f:
    f.write(py_final)

# vocab.json 도 같이 저장
with open("output/vocab.json", "w", encoding="utf-8") as f:
    json.dump(vocab, f, ensure_ascii=False, indent=2)

# 새 이름으로 복사 -> 다운로드 트리거
import shutil
shutil.copy("output/vocab_stairs.py", "output/vocab_stairs_v5.py")
shutil.copy("output/vocab.json",      "output/vocab_v5.json")
print("Saved! vocab_stairs_v5.py /", len(py_final), "chars")
print("Saved! vocab_v5.json /", len(vocab), "words")
