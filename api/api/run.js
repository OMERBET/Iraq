const IBM_51Q = {
  avg_gate_error: 0.000842,
  avg_readout_error: 0.0325,
  t1_relaxation_us: 145.2,
  t2_coherence_us: 122.8
};

function noise(bit) {
  const err = IBM_51Q.avg_readout_error + IBM_51Q.avg_gate_error * 51;
  return Math.random() < err ? (Math.random() > 0.5 ? 1 : 0) : bit;
}

export default function handler(req, res) {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "POST,OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  if (req.method === "OPTIONS") return res.status(200).end();

  const shots = 1024;
  const counts = {};
  for (let i = 0; i < shots; i++) {
    let s = "";
    for (let q = 0; q < 3; q++) s += noise(Math.random() > 0.5 ? 1 : 0);
    counts[s] = (counts[s] || 0) + 1;
  }

  const output = `=== IBM 51Q Simulation ===\nالنتائج: ${JSON.stringify(counts)}\nT1: ${IBM_51Q.t1_relaxation_us}μs | T2: ${IBM_51Q.t2_coherence_us}μs`;
  res.status(200).json({ output, counts, success: true, error: "" });
}
