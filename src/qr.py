"""Styled QR code as inline SVG: round dots, rounded finder patterns, brand ink on transparent — for the deck and the site."""
import segno

def qr_svg(url, size=120, ink="#141414", cls="qr"):
    q = segno.make(url, error="m")
    m = q.matrix; n = len(m); quiet = 1
    total = n + quiet * 2
    cell = size / total
    out = [f'<svg class="{cls}" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size:.2f} {size:.2f}" width="{size}" height="{size}" role="img" aria-label="QR-код: {url}">']
    finders = [(0, 0), (0, n - 7), (n - 7, 0)]
    def in_finder(r, c):
        return any(fr <= r < fr + 7 and fc <= c < fc + 7 for fr, fc in finders)
    for fr, fc in finders:
        x = (fc + quiet) * cell; y = (fr + quiet) * cell; s = 7 * cell
        out.append(f'<rect x="{x:.2f}" y="{y:.2f}" width="{s:.2f}" height="{s:.2f}" rx="{cell * 2:.2f}" fill="none" stroke="{ink}" stroke-width="{cell:.2f}" transform="translate({cell / 2:.2f} {cell / 2:.2f}) scale({(s - cell) / s:.4f})" />')
        out.append(f'<rect x="{x + 2 * cell:.2f}" y="{y + 2 * cell:.2f}" width="{3 * cell:.2f}" height="{3 * cell:.2f}" rx="{cell * 0.9:.2f}" fill="{ink}" />')
    r_dot = cell * 0.42
    for r in range(n):
        for c in range(n):
            if m[r][c] and not in_finder(r, c):
                out.append(f'<circle cx="{(c + quiet + .5) * cell:.2f}" cy="{(r + quiet + .5) * cell:.2f}" r="{r_dot:.2f}" fill="{ink}" />')
    out.append("</svg>")
    return "".join(out)

if __name__ == "__main__":
    print(qr_svg("https://t.me/OBIIMY_sales")[:200])
