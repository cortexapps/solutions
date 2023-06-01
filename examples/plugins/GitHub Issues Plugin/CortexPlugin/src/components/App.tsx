import React from "react";

import "../baseStyles.css";
import { CortexApi } from "@cortexapps/plugin-core";

const getServiceTag = async (): Promise<string> => {
  const context = await CortexApi.getContext();
  // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
  const serviceTag = context.entity!.tag;
  // eslint-disable-next-line @typescript-eslint/no-unnecessary-type-assertion
  return serviceTag as string;
};


const App: React.FC = () => {
  const [posts, setPosts] = React.useState<any[]>([]);
  React.useEffect(() => {
    const fetchData = async (): Promise<void> =>{
      const cortexTag = await getServiceTag();
      console.log(cortexTag)
      const result = await CortexApi.proxyFetch(`https://api.getcortexapp.com/api/v1/catalog/${cortexTag}/openapi`);
      const resultJson = await result.json();
      console.log({resultJson})
      const ghRepo: string = resultJson.info['x-cortex-git'].github.repository;
      console.log(ghRepo)
      const iResult = await CortexApi.proxyFetch(`https://api.github.com/repos/${ghRepo}/issues?direction=asc`);
      const jResult = await iResult.json();
      console.log({jResult})
      setPosts(jResult);
    };
    void fetchData();

  }, []);

  
 

  return (
    <div className="posts-container">
      <table >
        <tr>
          <th>Number</th>
          <th>Short Description</th>
          <th>State</th>
        </tr>
        {posts.map((post) => {
          return (
            <tr key={post.number}>
              <td>{post.number}</td>
              <td>{post.title}</td>
              <td >{post.state}</td>
            </tr>
          );
        })}
      </table>
    </div>
  );
};

export default App;
