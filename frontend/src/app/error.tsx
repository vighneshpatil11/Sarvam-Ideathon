"use client";
import { useEffect } from "react"; import { AlertTriangle } from "lucide-react";
export default function GlobalError({error,reset}:{error:Error&{digest?:string};reset:()=>void}){useEffect(()=>{console.error("SAARTHI UI error",error.digest);},[error]);return <div className="container page-container not-found"><AlertTriangle size={42}/><h1>Something went wrong.</h1><p>The page could not be displayed. Please try again.</p><button className="button button-primary" onClick={reset}>Try again</button></div>}
