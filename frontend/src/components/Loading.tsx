import { Loader } from "@/components/ui/loader";

const Loading = () => {
    return (
        <Loader variant="dual-ring" className="w-max m-auto">
            <span className="text-black dark:text-white">Please wait ...</span>
        </Loader>
    )
}

export default Loading
