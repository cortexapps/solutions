import React from "react";
import { CortexApi } from "@cortexapps/plugin-core";
import "../baseStyles.css";

// import ErrorBoundary from "./ErrorBoundary";

 const getServiceName = async (): Promise<string> => {
   const context = await CortexApi.getContext();
   // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
   const serviceName = context.entity!.name;
   return serviceName as string;
 };

const App: React.FC = () => {
  const [posts, setPosts] = React.useState<any[]>([]);
  React.useEffect(() => {
    const fetchData = async (): Promise<void> => {
      const cortexService = await getServiceName();
      console.log(cortexService)
      const result = await CortexApi.proxyFetch(
        `https://dev93537.service-now.com/api/now/table/cmdb_ci?sysparm_query=name%3D${cortexService}`
      );
      const resultJson = await result.json();
      console.log({resultJson})
      const sysId: string = resultJson.result[0].sys_id;
      const iResult = await CortexApi.proxyFetch(
        `https://dev93537.service-now.com/api/now/table/incident?sysparm_query=cmdb_ci%3D${sysId}`
      );
      const jResult = await iResult.json();
      console.log({jResult})
      setPosts(jResult.result);
    };
    void fetchData();
  }, []);

  return (
    <div className="posts-container">
      <table >
        <tr>
          <th>Short Description</th>
          <th>Priority</th>
        </tr>
        {posts.map((post) => {
          return (
            <tr key={post.number}>
              <td>{post.short_description}</td>
              <td >{post.priority}</td>
            </tr>
          );
        })}
      </table>
    </div>
  );
};

export default App;
