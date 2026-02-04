export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-br from-slate-900 to-slate-800 p-8">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-4xl font-bold text-white mb-4">RAG Document Q&A System</h1>
        <p className="text-slate-300 mb-8">
          Upload your documents and ask questions using local LLM powered by Ollama
        </p>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
            <h2 className="text-xl font-semibold text-white mb-3">Document Upload</h2>
            <p className="text-slate-400">
              Upload PDFs, TXT, DOCX and other document formats
            </p>
          </div>
          
          <div className="bg-slate-800 p-6 rounded-lg border border-slate-700">
            <h2 className="text-xl font-semibold text-white mb-3">Ask Questions</h2>
            <p className="text-slate-400">
              Get intelligent answers based on your document content
            </p>
          </div>
        </div>
      </div>
    </main>
  )
}
