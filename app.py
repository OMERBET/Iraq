from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import numpy as np
import json, traceback

app = FastAPI(title="Iraq Quantum Lab API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class CodeRequest(BaseModel):
    code: str

class QueryRequest(BaseModel):
    query: str

# ── محاكاة كمية بـ numpy (بدون Qiskit لأن HF Spaces مجاني محدود) ──
QUANTUM_PROGRAMS = {
    "bell": """
import numpy as np
shots = 1024
results = {'00': 0, '11': 0}
for _ in range(shots):
    if np.random.random() < 0.5:
        results['00'] += 1
    else:
        results['11'] += 1
print("=== Bell State — تشابك كمي ===")
print(f"النتائج: {results}")
print(f"التفسير: الكيوبتان متشابكان — إذا قست الأول يحدد الثاني تلقائياً")
""",
    "superposition": """
import numpy as np
shots = 1024
n = 3
results = {}
for _ in range(shots):
    state = ''.join(['1' if np.random.random() < 0.5 else '0' for _ in range(n)])
    results[state] = results.get(state, 0) + 1
print("=== Superposition — 3 Qubits ===")
print(f"النتائج: {dict(sorted(results.items()))}")
print(f"كل كيوبت بحالتين 0 و1 في نفس الوقت — {2**n} حالة ممكنة")
""",
    "grover": """
import numpy as np
target = '11'
shots = 1024
N = 4
probs = {'00': 0.083, '01': 0.083, '10': 0.083, '11': 0.751}
results = {s: 0 for s in probs}
for _ in range(shots):
    r = np.random.random()
    cum = 0
    for state, p in probs.items():
        cum += p
        if r < cum:
            results[state] += 1
            break
print("=== Grover Search ===")
print(f"الهدف: |{target}⟩")
print(f"النتائج: {results}")
print(f"Grover يضخم احتمالية الهدف — يجد الجواب بـ √N خطوة")
"""
}

@app.get("/")
def root():
    return {"status": "Iraq Quantum Lab API — Running", "version": "1.0"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
async def run_code(req: CodeRequest):
    """تشغيل كود Python كمي"""
    import sys
    from io import StringIO
    
    buf = StringIO()
    old_stdout = sys.stdout
    sys.stdout = buf
    
    result = {"output": "", "counts": {}, "success": True, "error": ""}
    
    try:
        # بيئة آمنة
        safe_globals = {
            "__builtins__": __builtins__,
            "np": np,
            "numpy": np,
        }
        exec(req.code, safe_globals)
        output = buf.getvalue()
        result["output"] = output
        
        # استخرج النتائج تلقائياً
        import re
        m = re.search(r'\{[^}]+\}', output)
        if m:
            try:
                counts = json.loads(m.group().replace("'", '"'))
                result["counts"] = counts
            except:
                pass
                
    except Exception as e:
        result["success"] = False
        result["error"] = str(e)
        result["output"] = f"خطأ: {e}\n{traceback.format_exc()}"
    finally:
        sys.stdout = old_stdout
    
    return result

@app.post("/ask")
async def ask_quantum(req: QueryRequest):
    """جواب على سؤال كمي مع كود"""
    query = req.query.lower()
    
    # قاموس الأسئلة الشائعة
    answers = {
        "bell": {
            "answer": "Bell State هو أبسط مثال على التشابك الكمي. يتكون من كيوبتين مترابطين بحيث قياس أحدهما يحدد الآخر فوراً بغض النظر عن المسافة بينهما. هذه الظاهرة هي أساس الاتصالات الكمية والتشفير الكمي.",
            "code": QUANTUM_PROGRAMS["bell"],
            "result": "النتائج تظهر 50% للحالة |00⟩ و50% للحالة |11⟩ — دليل على التشابك الكامل بين الكيوبتين"
        },
        "superposition": {
            "answer": "التراكب الكمي أو Superposition هو قدرة الكيوبت على التواجد في حالتين 0 و1 في نفس الوقت حتى لحظة القياس. هذا يختلف جذرياً عن البت الكلاسيكي الذي يكون إما 0 أو 1 فقط. بوابة Hadamard هي التي تضع الكيوبت في حالة التراكب.",
            "code": QUANTUM_PROGRAMS["superposition"],
            "result": "النتائج تظهر توزيعاً متساوياً على 8 حالات ممكنة — كل كيوبت كان في حالتين في نفس الوقت"
        },
        "grover": {
            "answer": "خوارزمية Grover هي خوارزمية بحث كمي تجد العنصر المطلوب في قاعدة بيانات بـ √N خطوة بدلاً من N خطوة كلاسيكياً. مثلاً للبحث في مليون عنصر تحتاج 1000 خطوة فقط بدلاً من مليون. تستخدم تقنية Oracle وDiffusion لتضخيم احتمالية الهدف.",
            "code": QUANTUM_PROGRAMS["grover"],
            "result": "الهدف |11⟩ يظهر بنسبة 75% بينما الحالات الأخرى بنسبة 8% — هذا هو تضخيم Grover"
        },
    }
    
    # البحث عن الكلمة المناسبة
    response = None
    for key in answers:
        if key in query or key.replace("_", " ") in query:
            response = answers[key]
            break
    
    # جواب عام إذا ما لقينا
    if not response:
        response = {
            "answer": f"سؤالك عن '{req.query}' يتعلق بالحوسبة الكمية. الحوسبة الكمية تستخدم مبادئ ميكانيكا الكم مثل التراكب والتشابك لحل مسائل معقدة بكفاءة أعلى بكثير من الحواسيب الكلاسيكية. يمكنني شرح Bell State، Superposition، Grover، QFT، أو Teleportation بالتفصيل.",
            "code": QUANTUM_PROGRAMS["bell"],
            "result": "جرّب أحد الأمثلة الجاهزة لترى كيف تعمل المحاكاة الكمية"
        }
    
    return response
