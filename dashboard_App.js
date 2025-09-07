import React, {useEffect, useState} from 'react';
function App(){
  const [summary,setSummary]=useState([]);
  useEffect(()=>{
    fetch("http://localhost:8000/reports/summary")
      .then(r=>r.json()).then(d=>setSummary(d.summary))
  },[]);
  return <div style={{padding:20}}>
    <h1>Health Dashboard</h1>
    <table border={1}><thead><tr><th>Village</th><th>Reports</th></tr></thead>
      <tbody>{summary.map((r,i)=><tr key={i}><td>{r[0]}</td><td>{r[1]}</td></tr>)}</tbody>
    </table>
  </div>
}
export default App;