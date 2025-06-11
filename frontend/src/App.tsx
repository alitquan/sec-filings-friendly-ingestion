import React, {useState} from "react";
import config from "./config.tsx";

function App() { 
    const [url, setUrl] = useState('');
    const [ticker,setTicker] = useState('');
    const [filedStatus, setFiledStatus] = useState(''); 
    const [fileData, setFileData] = useState('');
    const [outputFile, setOutputFile] = useState('')


    const handlePDFconversion = async(e) => {
        e.preventDefault(); 
        setFiledStatus("Attempting to convert "+url+" to PDF...");
        const endpoint = config.API_URL+"generatePDF-filing";
        try{ 
            const response = await (fetch (endpoint, {
                method: "POST",
                headers: {
                    "Content-Type":"application/json",
                },
                body: JSON.stringify({
                    url : url,
                    outputFile: outputFile,
                }),
            }))
            if (!response.ok) {
                setFiledStatus("Error retrieving filing") 
                return;
            }
            setFiledStatus("Submitting...");
            const data = await response.json();
            // open in new tab
            const pdfUrl = `${config.API_URL}download-pdf/${encodeURIComponent(data.filename)}`;
            window.open(pdfUrl, "_blank");

            console.log("/generatePDF-filing worked!");
            setFiledStatus("Download Successful ! ")
            return "OK";
            
        }
        catch (error) {
            console.error("PDF conversion failed:", error);
            setFiledStatus("Error occurred during conversion");
        }
    }



    const handleSubmit2 = async (e) => {
        e.preventDefault();
        console.log("Submitted URL: ", url);
        setFiledStatus(url); 

        const endpoint = config.API_URL+"getFiling";
        console.log(endpoint)
        const wantsDownload = true 
        try {
            const response = await fetch(endpoint, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    ticker: ticker,
                    download: wantsDownload,
                }),
            });
            if (!response.ok) {
                setFiledStatus("Error retrieving filing") 
            }
            if (wantsDownload) {
                console.log("Download struck")
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const link = document.createElement("a");
                link.href = url;
                link.click();
                window.URL.revokeObjectURL(url);
                setFiledStatus("Success: File downloaded!");
            } else {
                const data = await response.json();
                setFiledStatus("Success: Filing received!");
                setFileData(data.fileContents);
            }
        } catch (error) {
            console.error("Error:", error);
            setFiledStatus("Error: Failed to submit data.");
        }
    } 


    return(
        <div className="min-h-screen flex items-center justify-center bg-gray-100"> 
            <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md"> 
                <h1 className="text-2xl font-semibold mb-4 text-center"> Convert SEC URLs to PDF: </h1> 
                <form onSubmit={handlePDFconversion} className="flex flex-col space-y-4"> 
                    <div className="bg-white p-8 w-full max-w-md flex flex-col space-y-2 justify-center">
                        <input 
                            type="text" 
                            placeholder="Enter URL Here"
                            className="p-3 border rounded-md"
                            value={url} 
                            onChange={(e)=> setUrl(e.target.value)}
                            required
                        /> 

                    </div> 

                      <div className="bg-white p-8 w-full max-w-md flex flex-col space-y-2 justify-center">
                        <input 
                            type="text" 
                            placeholder="Enter Output Filename Here"
                            className="p-3 border rounded-md"
                            value={outputFile} 
                            onChange={(e)=> setOutputFile(e.target.value)}
                            required
                        /> 
                    </div> 
                    
                    <button
                        type="submit"
                        className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition" 
                    > 
                        Get PDF of Filing
                    </button> 
                </form> 
                { filedStatus && 
                (
                    <div className="mt-4 text-center text-sm text-gray-700" >
                        {filedStatus} 
                    </div> 
                )
                }
            </div> 
        </div>


    ) 
} 

export default App; 

