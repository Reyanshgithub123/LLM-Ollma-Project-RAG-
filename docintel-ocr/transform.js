function transform(result, docId) {

  const output = {
    doc_id: docId,
    pages: [],
    processed_at: new Date().toISOString()
  };

  result.pages.forEach((page, i) => {

    const pageObj = {
      page_no: i + 1,
      width: page.width,
      height: page.height,
      lines: [],
      tables: []
    };

    // Extract text lines
    page.lines.forEach(line => {
      pageObj.lines.push({
        text: line.content,
        bbox: line.polygon
      });
    });

    // Extract tables
    result.tables?.forEach(table => {

      if (table.boundingRegions[0].pageNumber === i + 1) {

        const rows = Array
          .from({ length: table.rowCount }, () => []);

        table.cells.forEach(cell => {
          rows[cell.rowIndex][cell.columnIndex] =
            cell.content;
        });

        pageObj.tables.push({
          rows,
          bbox: table.boundingRegions[0].polygon
        });
      }
    });

    output.pages.push(pageObj);
  });

  return output;
}

module.exports = transform;
