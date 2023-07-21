import React from "react";

import "../baseStyles.css";
import { CortexApi } from "@cortexapps/plugin-core";
import { Box, Text, SimpleTable } from "@cortexapps/plugin-core/components";

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
      const result = await CortexApi.proxyFetch(`http://api.getcortexapp.mooretex.com/api/v1/catalog/${cortexTag}/openapi`);
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

  const config = { 
    columns: [{
      Cell: (number: string) => <Box ><Text>{number}</Text></Box>,
      accessor: 'number',
      id: 'number',
      title: 'Number',
      width: '10%'
    }, {
      Cell: (title: string) => <Box><Text>{title}</Text></Box>,
      accessor: 'title',
      id: 'title',
      title: 'Short Description',
      width: '65%'
    }, {
      Cell: (state: string) => <Box justifyContent={'center'}><Text>{state}</Text></Box>,
      accessor: 'state',
      id: 'state',
      title: 'State',
    }]
  }
 

  return (
    <div className="posts-container">
      <SimpleTable config={config} items={posts} />
    </div>
  );
};

export default App;
