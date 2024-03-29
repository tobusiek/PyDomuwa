import React, { useEffect, useState } from "react";
import logo from "./logo.svg";
import "./App.css";
import axios, { AxiosResponse } from "axios";

const App: React.FC = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response: AxiosResponse = await axios.get(
          "http://localhost:2137/",
          {
            headers: {
              "Access-Control-Allow-Origin": "*",
              "X-Session-Key": "guccitrip",
            },
          },
        );
        setData(response.data);
      } catch (error) {
        console.log("Error", error);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Edit <code>src/App.tsx</code> and save to reload.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        {data ? <p>API Ping: {data}</p> : <p>no data</p>}
      </header>
    </div>
  );
};

export default App;
