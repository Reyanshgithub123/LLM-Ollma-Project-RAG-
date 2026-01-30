function makeChunks(data, docId) {

  const chunks = [];

  data.pages.forEach(page => {

    let buffer = "";

    page.lines.forEach(line => {

      buffer += line.text + " ";

      // Har ~500 chars pe ek chunk
      if (buffer.length > 500) {

        chunks.push({
          content: buffer.trim(),
          doc_id: docId,
          page: page.page_no
        });

        buffer = "";
      }
    });

    if (buffer.length > 0) {
      chunks.push({
        content: buffer.trim(),
        doc_id: docId,
        page: page.page_no
      });
    }

  });

  return chunks;
}

module.exports = makeChunks;
