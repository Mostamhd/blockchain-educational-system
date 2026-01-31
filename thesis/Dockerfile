# Use the official TeX Live image (full distribution)
FROM texlive/texlive:latest

# Install Noto fonts for Arabic support and other utilities
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    fonts-noto \
    fonts-noto-core \
    fonts-noto-extra \
    fonts-noto-ui-core \
    latexmk \
    && rm -rf /var/lib/apt/lists/*

# Update font cache
RUN fc-cache -f -v

# Set working directory
WORKDIR /workdir

# Default command: Compile using latexmk
# -pdfxe: Use xelatex
# -bibtex: Run bibtex
# -interaction=nonstopmode: Don't stop on errors
# -outdir=.: Output to current directory
CMD ["latexmk", "-pdfxe", "-bibtex", "-interaction=nonstopmode", "main.tex"]
