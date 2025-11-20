"""
Utility functions for the Bowtie Diagram
"""

UTILS_JS = """
const uid = (p) => p + '-' + Math.random().toString(36).slice(2,7);

/* Helper function to wrap text */
function wrapText(text, maxWidth) {
  const words = text.split(' ');
  const lines = [];
  let currentLine = words[0] || '';

  for (let i = 1; i < words.length; i++) {
    const testLine = currentLine + ' ' + words[i];
    if (testLine.length * 7 < maxWidth) {
      currentLine = testLine;
    } else {
      lines.push(currentLine);
      currentLine = words[i];
    }
  }
  lines.push(currentLine);
  return lines;
}
"""