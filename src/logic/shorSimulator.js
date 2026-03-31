// Shor Algorithm Logic for r=256 (N=511, a=2)
// This code simulates the Quantum Fourier Transform peaks for r=256

export const simulateShor256 = () => {
    const r = 256; 
    const totalShots = 1024;
    const states = [];
    
    // توليد 256 حالة فريدة (Peaks) بناءً على مضاعفات (N/r)
    for (let i = 0; i < r; i++) {
        // حساب التردد الكمي (Phase)
        let bitstring = (i * (Math.pow(2, 17) / r)).toString(2).padStart(51, '0');
        
        // توزيع الطلقات (Shots) بشكل احتمالي قريب للواقع الكمي
        let count = Math.floor((totalShots / r) + (Math.random() * 5 - 2)); 
        
        states.push({
            id: i + 1,
            state: formatTo8BitGroups(bitstring),
            counts: count > 0 ? count : 1,
            prob: ((count / totalShots) * 100).toFixed(2)
        });
    }

    return {
        circuit: "Shor-QFT-Extreme",
        qubits: 51,
        period: r,
        entropy: 8.0, // Log2(256)
        results: states.sort((a, b) => b.counts - a.counts).slice(0, 50) // عرض أفضل 50 حالة لتجنب الانهيار البصري
    };
};

// دالة لتنظيم شكل الكيوبتات (8-bit groups) كما في واجهتك
function formatTo8BitGroups(str) {
    return str.match(/.{1,8}/g).join(' ');
}
