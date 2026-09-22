export default function Loader({ message = 'Analyzing repository...' }) {
  return (
    <div className="flex flex-col items-center justify-center py-20 gap-6">
      <div className="relative w-16 h-16">
        <div className="absolute inset-0 rounded-full border-4 border-primary-900"></div>
        <div className="absolute inset-0 rounded-full border-4 border-t-primary-500 animate-spin"></div>
      </div>
      <div className="text-center">
        <p className="text-white font-semibold text-lg">{message}</p>
        <p className="text-gray-400 text-sm mt-1">This may take a few seconds...</p>
      </div>
    </div>
  )
}
