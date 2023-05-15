import React from 'react';
import { CortexApi } from '@cortexapps/plugin-core';
import "../baseStyles.css";

//import ErrorBoundary from "./ErrorBoundary";

const App = () => {
   const [posts, setPosts] = React.useState<any[]>([]);
   React.useEffect(() => {
      CortexApi.proxyFetch('https://dev93537.service-now.com/api/now/table/incident?sysparm_limit=10')
         .then((response) => response.json())
         .then((data) => {
            setPosts(data.result);            
         })
         .catch((err) => {
            console.log(err.message);
         });
       
   }, []);
   return (
   
        <div className="posts-container">
         <table border={1}>
            <tr>
               <th>Short Description</th>
               <th>Priority</th>
            </tr>
               {posts.map((post) => {
                return (
            <tr key={post.number}>
               <td>{post.short_description}</td>
               <td>{post.priority}</td>
            </tr>
       
                  );
               })}
         </table>
        </div>
    );
};    

export default App;
