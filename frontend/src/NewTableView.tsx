import React, {useState} from "react";
import config from "./config.tsx";

function NewTableView() { 

    // url & setUrl refer to URL used during downloads
    const [url, setUrl] = useState('');
    const [ticker,setTicker] = useState('');
    const [formType,setFormType] = useState('');
    const [filedStatus, setFiledStatus] = useState(''); 
    const [fileData, setFileData] = useState('');

    const handleSubmit = async (e) => {
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
                    formType: formType,
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
                link.download = ticker.toUpperCase() + "---" + formType + ".txt";
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
                <h1 className="text-2xl font-semibold mb-4 text-center"> Enter a Ticker + Form Type: </h1> 
                <form onSubmit={handleSubmit} className="flex flex-col space-y-4"> 
                    <div className="bg-white p-8 w-full max-w-md flex flex-col space-y-2 justify-center">
                        <input 
                            type="text" 
                            placeholder="APPL"
                            className="p-3 border rounded-md"
                            value={ticker} 
                            onChange={(e)=> setTicker(e.target.value)}
                            required
                        /> 

                        <select
                            className="p-3 border rounded-md"
                            value={formType}
                            onChange={(e) => setFormType(e.target.value)}
                            required
                        >
                        <option value="">Select Filing Type</option>
                        <option value="10-Q">10-Q</option>
                        <option value="10-K">10-K</option>
                        <option value="8-K">8-K</option>
                        <option value="S-1">S-1</option>
                        <option value="13D">13D</option>
                        <option value="13G">13G</option>
                        </select>


                    </div> 
                    <button
                        type="submit"
                        className="bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition" 
                    > 
                        Look For Filing 
                    </button> 
                </form> 
                { filedStatus && 
                (
                    <div className="mt-4 text-center text-sm text-gray-700" >
                        <p> Ticker: <strong> {ticker}</strong> </p> 
                        <p> Filing Type: <strong> {formType}</strong> </p> 
                    </div> 
                )
                }
            </div> 
        </div>


    ) 
} 

export default NewTableView; 

