import math
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    t_min: float = 0.0
    t_max: float = 3.0
    dt: float = 0.002
    x_min: float = -2.5
    x_max: float = 0.2
    out_dir: Path = Path(__file__).resolve().parents[1] / "results"


def k1(x0: float) -> float:
    q = 1.0 + x0 * x0
    return 2.0 * q / (1.0 + (1.0 + q * q) * (1.0 + q * q))


def k2(t0: float) -> float:
    e = math.exp(-t0)
    return 2.0 * e / (2.0 + 2.0 * e * e + e**4)


def frange(start: float, stop: float, step: float):
    v = start
    while v <= stop + 1e-12:
        yield v
        v += step


def make_characteristics(cfg: Config):
    x0_values = [0, -0.25, -0.5, -0.75, -1.0, -1.5, -2.0]
    t0_values = [0, 0.25, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0]
    t_grid = list(frange(cfg.t_min, cfg.t_max, cfg.dt))

    curves_c1 = []
    for x0 in x0_values:
        pts = [(t, x0 - k1(x0) * t) for t in t_grid]
        curves_c1.append((x0, pts))

    curves_c2 = []
    for t0 in t0_values:
        pts = [(t, -(t - t0) * k2(t0)) for t in t_grid]
        curves_c2.append((t0, pts))

    return curves_c1, curves_c2


def detect_intersections(curves_c1, curves_c2, eps=1e-3):
    intersections = []
    for x0, pts1 in curves_c1:
        for t0, pts2 in curves_c2:
            best = min(((abs(a[1] - b[1]), a[0], a[1]) for a, b in zip(pts1, pts2)), key=lambda z: z[0])
            if best[0] < eps:
                intersections.append((x0, t0, best[1], best[2], best[0]))
    return intersections


def map_to_canvas(t, x, cfg: Config, w=1200, h=800, pad=70):
    px = pad + (t - cfg.t_min) / (cfg.t_max - cfg.t_min) * (w - 2 * pad)
    py = h - pad - (x - cfg.x_min) / (cfg.x_max - cfg.x_min) * (h - 2 * pad)
    return px, py


def polyline(points, color, width):
    p = " ".join(f"{x:.2f},{y:.2f}" for x, y in points)
    return f'<polyline points="{p}" fill="none" stroke="{color}" stroke-width="{width}"/>'


def build_svg(cfg: Config, curves_c1, curves_c2):
    w, h = 1200, 800
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}">']
    parts.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')

    # axes
    x0, y0 = map_to_canvas(cfg.t_min, cfg.x_min, cfg, w, h)
    x1, _ = map_to_canvas(cfg.t_max, cfg.x_min, cfg, w, h)
    _, y1 = map_to_canvas(cfg.t_min, cfg.x_max, cfg, w, h)
    parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y0}" stroke="black"/>')
    parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y1}" stroke="black"/>')
    parts.append('<text x="600" y="40" font-size="24" text-anchor="middle">Task 1 var 8: characteristics crossing</text>')
    parts.append('<text x="1150" y="760" font-size="18">t</text>')
    parts.append('<text x="40" y="80" font-size="18">x</text>')

    for _, pts in curves_c1:
        c = [map_to_canvas(t, x, cfg, w, h) for t, x in pts]
        parts.append(polyline(c, "#1f77b4", 1.4))
    for _, pts in curves_c2:
        c = [map_to_canvas(t, x, cfg, w, h) for t, x in pts]
        parts.append(polyline(c, "#d62728", 1.2))

    parts.append('</svg>')
    return "\n".join(parts)


def write_summary(cfg: Config, intersections, curves_c1, curves_c2):
    out = cfg.out_dir / "summary.txt"
    with out.open("w", encoding="utf-8") as f:
        f.write("Task 1, var 8 — numerical postprocessing summary\n")
        f.write(f"time grid: [{cfg.t_min}, {cfg.t_max}] step={cfg.dt}\n")
        f.write(f"family-1 curves: {len(curves_c1)}\n")
        f.write(f"family-2 curves: {len(curves_c2)}\n")
        f.write(f"detected intersections (eps=1e-3): {len(intersections)}\n\n")
        for i, (x0, t0, t_star, x_star, err) in enumerate(intersections[:30], start=1):
            f.write(f"{i:02d}) x0={x0:>5.2f}, t0={t0:>5.2f}, t*={t_star:>7.4f}, x*={x_star:>8.5f}, |dx|={err:.2e}\n")


def main():
    cfg = Config()
    cfg.out_dir.mkdir(parents=True, exist_ok=True)
    curves_c1, curves_c2 = make_characteristics(cfg)
    intersections = detect_intersections(curves_c1, curves_c2)

    svg = build_svg(cfg, curves_c1, curves_c2)
    (cfg.out_dir / "characteristics_crossing.svg").write_text(svg, encoding="utf-8")
    write_summary(cfg, intersections, curves_c1, curves_c2)
    print(f"Done. intersections={len(intersections)}")


if __name__ == "__main__":
    main()
