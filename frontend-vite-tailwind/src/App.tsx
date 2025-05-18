import React, {useState} from "react";


function App() { 
    const [url, setUrl] = useState('');
    const [submittedUrl, setSubmittedUrl] = useState(null); 

    const handleSubmit = (e) => {
        e.preventDefault();
        console.log("Submitted URL: ", url);
        setSubmittedUrl(url); 
    } 


    return(
        <div className="min-h-screen flex items-center justify-center bg-gray-100"> 
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md"> 
                <h1 className="text-2xl font-semibold mb-4 text-center"> Enter a URL to Parse </h1> 
                <form onSubmit={handleSubmit} className="flex flex-col space-y-4"> 
                    <input
                        type="url"
                        placeholder="https://example.com"
                        className="p-3 border rounded-md"
                        value={url} 
                        onChange={(e)=> setUrl(e.target.value)}
                        required
                    /> 
                    <button
                        type="submit"
                        className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition" 
                    > 
                        Parse URL
                    </button> 
                </form> 
                { submittedUrl && 
                (
                    <div className="mt-4 text-center text-sm text-gray-700" >
                        <p> Submitted URL: <strong> {submittedUrl}</strong> </p> 
                        <p> Processing... (simulate backend work)</p> 
                    </div> 
                )
                }
            </div> 
        </div>


    ) 
} 

export default App; 

