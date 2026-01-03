use pyo3::prelude::*;

#[pyfunction]
fn motif_variance(motif: Vec<f32>) -> PyResult<f32> {
    let n = motif.len() as f32;
    if n == 0.0 { return Ok(0.0); }
    let mean = motif.iter().sum::<f32>() / n;
    let mut acc = 0.0f32;
    for x in motif.iter() { let d = *x - mean; acc += d * d; }
    Ok(acc / n.max(1.0))
}

#[pyfunction]
fn tempo_align(a: Vec<f32>, b: Vec<f32>) -> PyResult<f32> {
    let n = a.len(); let m = b.len();
    let mut dp = vec![f32::INFINITY; (n+1)*(m+1)];
    let idx = |i:usize, j:usize| -> usize { i*(m+1) + j };
    dp[idx(0,0)] = 0.0;
    for i in 1..=n {
        for j in 1..=m {
            let cost = (a[i-1] - b[j-1]).abs();
            let best = dp[idx(i-1,j)].min(dp[idx(i,j-1)]).min(dp[idx(i-1,j-1)]);
            dp[idx(i,j)] = cost + best;
        }
    }
    Ok(dp[idx(n,m)])
}

#[pymodule]
fn rust_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(motif_variance, m)?)?;
    m.add_function(wrap_pyfunction!(tempo_align, m)?)?;
    Ok(())
}
