import React, { useState, useEffect } from "react";
import dbConnect from "../../src/config";

export function NewsList() {
  const [news, setNews] = useState([]);

  useEffect(() => {
    const fetchNews = async () => {
      try {
        const response = await dbConnect.get("/feed/feed");
        setNews(response.data);
      } catch (error) {
        console.error("Error fetching news:", error);
      }
    };

    fetchNews();
  }, []);

  return (
    <div>
      <h1>Noticias</h1>

      {news.length > 0 ? (
        <ul>
          {news.map((item) => (
            <li key={item.id}>
              <h3>{item.title}</h3>
              <p>{item.feed}</p>
            </li>
          ))}
        </ul>
      ) : (
        <p>Cargando noticias...</p>
      )}
    </div>
  );
}
