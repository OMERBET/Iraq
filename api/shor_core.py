"""
=============================================================
  Iraq Quantum Lab — Shor's Algorithm (Optimized)
  سجل العلمي: Nielsen & Chuang (2010), Chapter 5
=============================================================
"""

import numpy as np
from math import gcd, ceil, log2
from fractions import Fraction
from collections import Counter


# ── 1. QFT via FFT ──────────────────────────

def qft_vector(state_vec):
    """QFT على state vector = DFT مُطبَّع"""
    N = len(state_vec)
    return np.fft.fft(state_vec) / np.sqrt(N)

def inverse_qft_vector(state_vec):
    """IQFT = QFT† = inverse DFT مُطبَّع"""
    N = len(state_vec)
    return np.fft.ifft(state_vec) * np.sqrt(N)


# ── 2. QUANTUM PERIOD FINDING ───────────────

def quantum_period_finding(a, N, shots=1024, noise_level=0.0):
    """
    محاكاة دقيقة لـ Period Finding الكمي.
    
    الدائرة (Nielsen & Chuang §5.3):
      |0⟩^(2n) ──H──[U_f]──IQFT──M
    
    حيث U_f: |x⟩|0⟩ → |x⟩|a^x mod N⟩
    بعد القياس على work register:
      |ψ⟩ = (1/√r) Σ_k |x₀ + k·r⟩
    ثم IQFT تحوّله إلى أسنان حادة عند مضاعفات Q/r
    """
    n = ceil(log2(N + 1))
    n_count = 2 * n
    Q = 2 ** n_count

    # الدورية الحقيقية
    true_r = None
    for r in range(1, N + 1):
        if pow(int(a), int(r), int(N)) == 1:
            true_r = r
            break

    measurements = []

    for _ in range(shots):
        if not true_r:
            measurements.append(0)
            continue

        # اختيار x₀ عشوائي — تمثّل قيمة work register المقاسة
        x0 = np.random.randint(0, true_r)

        # بناء state vector دوري: |ψ⟩ = (1/√M) Σ_{k} |x₀ + k·r⟩
        state = np.zeros(Q, dtype=complex)
        k = 0
        x = x0
        while x < Q:
            state[x] = 1.0
            x += true_r
            k += 1
        if k > 0:
            state /= np.sqrt(k)

        # تطبيق IQFT
        state = inverse_qft_vector(state)

        # ضوضاء IBM Eagle
        if noise_level > 0:
            nr = np.random.normal(0, noise_level / 2, Q)
            ni = np.random.normal(0, noise_level / 2, Q)
            state += (nr + 1j * ni)

        # قياس
        probs = np.abs(state) ** 2
        s = probs.sum()
        if s == 0:
            measurements.append(0)
            continue
        probs /= s

        measurements.append(int(np.random.choice(Q, p=probs)))

    return measurements, n_count


# ── 3. CONTINUED FRACTIONS ──────────────────

def continued_fractions(measured, Q, N):
    """
    استخراج r من القياس باستخدام الكسور المستمرة.
    measured/Q ≈ s/r  =>  نجد r
    """
    if measured == 0 or Q == 0:
        return None
    frac = Fraction(int(measured), int(Q)).limit_denominator(int(N))
    r = frac.denominator
    return r if 1 < r <= N else None


# ── 4. SHOR'S ALGORITHM ─────────────────────

def shor_algorithm(N, shots=1024, noise_level=0.0175):
    """
    خوارزمية Shor الكاملة (Nielsen & Chuang, Algorithm 5.2)
    
    1. N زوجي → عامل 2
    2. اختر a عشوائي
    3. GCD(a,N) > 1 → عامل مباشر
    4. Period Finding كمي → r
    5. r زوجي و a^(r/2) ≢ -1 → العوامل من GCD
    """
    log = [f"=== Shor — N={N} ==="]

    if N % 2 == 0:
        return {"success": True, "p": 2, "q": N // 2,
                "method": "trivial_even",
                "log": log + ["N زوجي → عامل 2"]}

    for attempt in range(12):
        a = np.random.randint(2, N)
        log.append(f"\nمحاولة {attempt+1}: a={a}")

        g = gcd(int(a), int(N))
        if g > 1:
            log.append(f"  GCD({a},{N})={g} → عامل مباشر")
            return {"success": True, "p": g, "q": N // g,
                    "a": int(a), "method": "gcd_direct",
                    "attempts": attempt + 1, "log": log}

        log.append(f"  تشغيل Period Finding ({shots} shot)...")
        measurements, n_count = quantum_period_finding(
            a, N, shots=shots, noise_level=noise_level)
        Q = 2 ** n_count

        counts = Counter(measurements)
        log.append(f"  أعلى نتائج: {dict(counts.most_common(4))}")

        seen_r = set()
        for m, _ in counts.most_common(30):
            if m == 0:
                continue
            r = continued_fractions(m, Q, N)
            if not r or r in seen_r:
                continue
            seen_r.add(r)

            if pow(int(a), int(r), int(N)) != 1:
                continue
            log.append(f"  r={r} — تم التحقق: {a}^{r} mod {N}=1")

            if r % 2 != 0:
                log.append("  r فردية — نتجاوز")
                continue

            x = pow(int(a), int(r) // 2, int(N))
            if x == N - 1:
                log.append("  a^(r/2)≡-1 — نتجاوز")
                continue

            p = gcd(x - 1, int(N))
            q = gcd(x + 1, int(N))

            if p > 1 and q > 1 and p * q == N:
                log.append(f"  ✓ {N} = {p} × {q}")
                return {
                    "success":    True,
                    "p":          p,
                    "q":          q,
                    "a":          int(a),
                    "period_r":   int(r),
                    "Q":          int(Q),
                    "n_count":    n_count,
                    "shots":      shots,
                    "noise_pct":  round(noise_level * 100, 2),
                    "method":     "quantum_period_finding",
                    "attempts":   attempt + 1,
                    "top_counts": dict(counts.most_common(8)),
                    "log":        log,
                    "verified":   f"{p} × {q} = {p*q}"
                }

    log.append("✗ فشل 12 محاولة — أعد التشغيل (الخوارزمية احتمالية)")
    return {"success": False, "log": log,
            "message": "Shor خوارزمية احتمالية — أعد المحاولة"}


# ── 5. IBM EAGLE NOISE ──────────────────────

IBM_EAGLE_51Q = {
    "avg_gate_error":    0.000842,
    "avg_readout_error": 0.0325,
    "t1_us":             145.2,
    "t2_us":             122.8,
}

def get_noise_level(n_qubits=51):
    return (IBM_EAGLE_51Q["avg_readout_error"]
            + IBM_EAGLE_51Q["avg_gate_error"] * n_qubits)


# ── 6. CLI TEST ──────────────────────────────

if __name__ == "__main__":
    import sys
    N     = int(sys.argv[1]) if len(sys.argv) > 1 else 51
    shots = int(sys.argv[2]) if len(sys.argv) > 2 else 256
    noise = get_noise_level()

    print(f"N={N}  shots={shots}  noise={noise*100:.2f}%")
    result = shor_algorithm(N, shots=shots, noise_level=noise)

    for line in result.get("log", []):
        print(line)

    print()
    if result["success"]:
        print(f"✓  {N} = {result['p']} × {result['q']}")
        if "period_r" in result:
            print(f"   r={result['period_r']}  a={result['a']}")
    else:
        print("✗", result.get("message"))
