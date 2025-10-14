import { RefreshCw } from "lucide-react"

interface ErrorBannerProps {
    title?: string
    description?: string
    retry?: () => void
    className?: string
}

export default function ErrorBanner({
    title = "Something went wrong",
    description = "An error occurred while processing your request.",
    retry,
    className = "",
}: ErrorBannerProps) {
    const handleRetry = () => {
        if (retry) {
            retry()
        } else {
            window.location.reload()
        }
    }

    return (
        <div className={`rounded-lg border border-red-200 bg-red-50 p-4 flex justify-between ${className}`}>
            <div className="flex flex-col items-start justify-between gap-2">
                <div>
                    <h3 className="text-2xl font-semibold text-red-800">{title}</h3>
                    <p className="text-sm text-red-700">{description}</p>
                </div>

                <button
                    onClick={handleRetry}
                    className="mt-2 inline-flex items-center gap-1.5 rounded-md bg-red-100 px-3 py-1.5 text-sm font-medium text-red-800 hover:bg-red-200 focus:outline-none focus:ring-2 focus:ring-red-600 focus:ring-offset-2"
                >
                    <RefreshCw className="h-4 w-4" />
                    Retry
                </button>
            </div>

            <img
                src="/error.png"
                alt="Error"
                width={150}
                height={150}
                className="flex-shrink-0"
            />
        </div>
    )
}

