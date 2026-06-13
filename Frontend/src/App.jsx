import { useState } from "react";
import { useRef } from "react";
import { useEffect } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:5000"

function App() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const resultRef = useRef(null);
  const [toast,setToast] = useState("")
  const [copied,setCopied] = useState("")
  const[tone,setTone] = useState("professional")
  const [history,setHistory] = useState([]);
  const[activeTab,setActiveTab] = useState("twitter")
  const[format,setFormat] = useState("social")
  const[userId,setUserId] = useState("");
  const[usage, setUsage] = useState(0)
  const[limit,setLimit] = useState(0)

  useEffect(() => {
    let id = localStorage.getItem("userId");

    if(!id){
      id = "user_" + Math.random().toString(36).substring(2,9);
      localStorage.setItem("userId",id);
    }
    setUserId(id);
  },[]);

  const handleImprove = async() => {
    if (!result) return ;

    setLoading(true);

    try{
      const res = await fetch(`${API_URL}/generate`,{
        method:"POST",
        headers:{
          "Content-Type":"application/json",
        },
        body:JSON.stringify({
          text,
          tone:"viral", //force viral
          format,
          userId,
        }),
      });
      const data = await res.json();

      if(data.usage !== undefined){
        setUsage(data.usage);
        setLimit(data.limit);
      }

      if(data.error){
        if(data.error === "limit_reached"){
          setToast("Limit Reached! Upgrade to Pro");
        }else{
          setToast("Error: " + data.error );
        }
        setLoading(false)
        return;
      }

      setResult(data);
      setToast("Improved!");
    }catch(err){
      setToast("improved Failed")
    }

    setLoading(false);
  }

//  Creating Download Function 
  const handleDownload = () => {
    if(!result) return ;

    let content ="";

    if(format === "social"){
      content = `TWITTER:\n${result.twitter?.join("\n\n")}
      LINKEDIN:\n${result.linkedin}

      SUMMARY: \n${result.summary}`;
    }
    if(format === 'email'){
      content = `SUBJECT:
      \n${result.subject}

      BODY:
      \n${result.body}`
    }
    if(format === 'instagram'){
      content = `CAPTION:
       \n${result.caption}

      HASHTAGS:
      \n${result.hashtags}`;
    }
    const blob = new Blob([content],{type:"text/plain"});
    const url = URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = `${format}-content.txt`;
    a.click();
    URL.revokeObjectURL(url)
  };
    

  const handleGenerate = async () => {
  if (!text.trim()) return;

  setLoading(true);

  if(text.length > 5000){
    setToast("Text too long (max 5000 chars)")
    setLoading(false)
    return 
  }

  try {
    const res = await fetch(`${API_URL}/generate`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text, tone, format, userId}),
    });

    const data = await res.json();

    if(data.usage !== undefined){
      setUsage(data.usage);
      setLimit(data.limit);
    }
    
    console.log("API RESPONSE:",data); //Debug

    if(data.error){
      if(data.error === "limit_reached"){
        setToast("Limit reached! Upgrade to Pro")
        setLimit(limit)
      }else{
        setToast("Error:" + data.error)
      }
      setLoading(false);
      return;
    }

    setResult(data);

    setHistory((prev) => [
      {
        text,
        result: data,
        tone,
        format,
        time: new Date().toLocaleTimeString(),
      },
      ...prev,
    ]);

  } catch (error) {
    console.error(error)
    setToast("Server Not Reachable");
  }

  setLoading(false);

  setTimeout(() => {
    resultRef.current?.scrollIntoView({ behavior: "smooth",block:"start" });
  }, 100);
};

  return (
    <div className="wrapper">
      <div className="container">

        {/* 🔥 HEADER */}
        <div className="header">
          <h1 className="gradient-text">EchoStream</h1>
          <p className="subtitle">
            Turn podcasts,blog,videos and newsletters into ready-to-post social content in seconds.
          </p>
          <div>
            <div>⚡ 5 Formats</div>
            <div>🚀 ~10 sec Generation</div>
            <div>🤖 AI Powered</div>
          </div>
        </div>
        <div className="beta-badge">
           🚀 Beta Launch
        </div>

        {/* 📝 INPUT SECTION */}
        <div className="input-section">
          <select className="tone-select" 
          value = {tone}
          onChange={(e) => setTone(e.target.value)}>
            <option value="professional">Professional</option>
            <option value="casual">Casual</option>
            <option value="viral">Viral</option>
          </select>
          <select 
            value = {format}
            onChange = {(e) => {
              setFormat(e.target.value);
              setActiveTab("twitter");
              setResult(null);  //clear old output
            }}
            className="format-select"
          >
            <option value="social">Social media</option>
            <option value="email">Email</option>
            <option value="instagram">Instagram</option>
          </select>
          <textarea
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Paste your transcript here..."
          />
           
          <p className="char-count">{text.length} characters</p>

          <p className="usage">Free Limit : 3 generation</p>

          <p className="usage">
            Uses left:{Math.max(limit-usage,0)}/{limit || 0}
            </p>

          <div className="button-group">
            <button
            onClick={handleGenerate}
            disabled={loading || !text.trim() || (limit > 0 && usage >= limit)}
          >
            {loading ? <span className="spinner"></span> : "Generate Content"}
          </button>
          
              <button onClick={handleImprove} disabled = {loading ||(limit > 0 && usage >= limit )}>
                Make it More Viral
              </button>
            </div>
        </div>
        {!result && !loading && (
          <div className="empty">
            <h3>✨ Create content for every platform from one transcript
              Paste a blog, podcasts transcript, newsletter or video script.
            </h3>
            <div className = "feature-list">
              <p>🐦Twitter Threads</p>
              <p>💼LinkedIn posts</p>
              <p>📧Emails</p>
              <p>📸Instagram Captions</p>
            </div>

            <span>Paste Your Transcript and generate in seconds</span>
          </div>
        )}
        

        {loading && (
          <div className="output">
            <p className = "loading-text">⚡ Generating content...</p>
            <div className = "output-card skeleton"></div>
            <div className="output-card skeleton"></div>
            <div className="output-card skeleton"></div>

          </div>
        )}

        {history.length > 0 && (
          <div className="history">
            <h3>History of generated Content</h3>

            {
              history.map((item,index) => (
                <div key = {index}
                className="history-item"
                onClick={() => {
                  setText(item.text);
                  setResult(item.result);
                  setTone(item.tone);
                  setFormat(item.format);  // default restore
                }}>
                  <p className="history-text">
                    {item.text.slice(0, 50)}...
                  </p>
                  <span className="history-meta">{item.tone} • {item.time}</span>
                </div>
              ))}
          </div>
        )}


        {/* 📦 OUTPUT SECTION */}
        {result && (
          <div className="output" ref={resultRef}>
            <div className="top-action">
              <button className="download-btn" onClick = {handleDownload}>
                Download
              </button>

            </div>

           
          
          <div className="tabs">
            {format === 'social' && (
              <>
            <button className={activeTab === "twitter" ? "active-tab":""}
            onClick={() => setActiveTab("twitter")}
            >Twitter
            </button>

            <button className={activeTab === "linkedin" ? "active-tab":""}
            onClick={() => setActiveTab("linkedin")}
            >Linkedin</button>

            <button className={activeTab === "summary" ? "active-tab":""}
            onClick={() => setActiveTab("summary")}>Summary
            </button>
            </>
            )}

            {format === 'email' && (
              <button className="active-tab">Email</button>
            )}

            {format === 'instagram' && (
              <button className="active-tab">Instagram</button>
            )}

          </div>

          {format === 'social' && activeTab === "twitter" && result.twitter && (
           <div className="output-card">
  <div className="card-header">
    <h3>🐦 Twitter Thread</h3>

    {/*// Adding best Hook Feature */}
    {result.twitter?.length > 0 && (
      <div className = "best-hook">
        Best Hook:{result.twitter[0]}
      </div>
    )}
    
    <button className="copy-btn" onClick={() => {
      const allTweets = result.twitter.join("\n\n");
      navigator.clipboard.writeText(allTweets);
      setCopied("twitter")
      setToast("Copied Full Thread!");
      setTimeout(() => {
        setCopied("");
        setToast("");
      },1500);
    }}>
     {copied === "twitter" ? "✅ Copied" : "Copy"}
    </button>
      
    </div>

  {/* 🔥 Tweets */}
  {Array.isArray(result.twitter) && result.twitter?.map((tweet, index) => (
      <div key={index} className="tweet">
        <div className="card-header">
          <h4>Tweet {index + 1}</h4>
          
        </div>

        {/* ✅ TEXT GOES HERE */}
        <pre>{tweet}</pre>
      </div>
    ))}
</div>)}

            {/* LinkedIn */}
            {format === 'social' && activeTab === "linkedin" && result.linkedin &&(
            <div className="output-card">
              <div className="card-header">
                <h3>💼 LinkedIn Post</h3>
                <button
                  className="copy-btn"



                  onClick={() =>
                    {navigator.clipboard.writeText(result.linkedin);
                      setCopied("linkedin");
                      setToast("Copied linkedin!");
                      setTimeout(() => {
                        setCopied("");
                        setToast("");},1500);
                    }}
                >
                  {copied === "linkedin" ? " ✅ Copied":"Copy"}
                </button>
              </div>
              <pre>{result.linkedin || " No content generated"}</pre>
            </div>)}

            {/* Summary */}
            {format === "social" && activeTab === "summary" && result.summary && (
            <div className="output-card">
              <div className="card-header">
                <h3>🧠 Summary</h3>
                <button
                  className="copy-btn"
                  onClick={() =>
                    {navigator.clipboard.writeText(result.summary);
                      setCopied("summary");
                      setToast("Copied Summary!");
                      setTimeout(() => {
                        setCopied("");
                        setToast("");},1500);

                    }}
                >
                  {copied === "summary" ? "✅ Copied" : "Copy"}
                </button>
              </div>
              <pre>{result.summary}</pre>
            </div>)}

            {format === 'email' && result?.subject && (
              <div className="output-card">
                <div className="card-header">
                  <h3>Email</h3>
                  <button className="copy-btn"
                  onClick={() =>{
                    navigator.clipboard.writeText(
                      `Subject:${result.subject}\n\n${result.body}`
                    );
                    setToast("Copied Email!");
                    setTimeout(() => setToast(""),1500);
                  }}>
                    Copy
                  </button>
                </div>
                <p><strong>Subject:</strong>{result.subject}</p>
                <pre>{result.body}</pre>
              </div>
            )}

            {format === 'instagram' && result?.caption && (
              <div className="output-card">
                <div className="card-header">
                  <h3>Instagram</h3>
                  <button className="copy-btn"
                  onClick={() => {
                    navigator.clipboard.writeText(
                      `${result.caption}\n\n${result.hashtags}`
                    );
                    setToast("Copied Instagram");
                    setTimeout(() => setToast(""),1500);
                  }}>
                   Copy
                  </button>
                </div>
                <pre>{result.caption}</pre>

                <div className="hashtags">
                  {result.hashtags?.split(" ").map((tag,i) => (
                    <span key={i}>{tag}</span>
                  ))}
                </div>
              </div>
            )}

          </div>
        )}


         {toast && <div className="toast">{toast}</div>}
      </div>
    </div>
  );
}

export default App;