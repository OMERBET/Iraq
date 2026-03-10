/* 
   IBM Quantum Calibration Data - 51 Qubit Emulator Model
   Source: Qiskit Runtime Fake Backends (IBM Eagle Architecture)
*/

const IBM_51Q_CALIBRATION = {
    avg_gate_error: 0.000842,    // نسبة خطأ البوابة المنطقية
    avg_readout_error: 0.0325,   // نسبة خطأ القراءة النهائية (Measurement)
    t1_relaxation_us: 145.2,     // زمن تلاشي الكيوبت (مايكرو ثانية)
    t2_coherence_us: 122.8       // زمن التماسك (مايكرو ثانية)
};

// الدالة الرياضية لتقوية نتائج المحاكاة وجعلها واقعية
function applyQuantumPhysics(idealBit) {
    // 1. حساب احتمالية الخطأ التراكمي لـ 51 كيوبت
    // معادلة: الخطأ الكلي = خطأ القراءة + (خطأ البوابات * عدد الكيوبتات)
    let cumulativeNoise = IBM_51Q_CALIBRATION.avg_readout_error + (IBM_51Q_CALIBRATION.avg_gate_error * 51);
    
    // 2. تطبيق العشوائية الفيزيائية (Quantum Noise)
    if (Math.random() < cumulativeNoise) {
        // هنا "تخرب" النتيجة مثل جهاز IBM الحقيقي
        return Math.random() > 0.5 ? 1 : 0; 
    }
    
    return idealBit; // النتيجة بقيت سليمة
}

console.log("✅ Quantum Noise Model (51-Qubit) Loaded Successfully.");
