import React from "react";

function Dashboard() {
//   const cards = [
//     { title: "Users", value: 1200, color: "primary" },
//     { title: "Orders", value: 350, color: "success" },
//     { title: "Revenue", value: "$12,500", color: "warning" },
//   ];

//   return (
//     <div className="container mt-4">
//       <div className="row">
//         {cards.map((card, index) => (
//           <div className="col-md-4 mb-4" key={index}>
//             <div className={`card text-white bg-${card.color} h-100`}>
//               <div className="card-body">
//                 <h5 className="card-title">{card.title}</h5>
//                 <h3>{card.value}</h3>
//               </div>
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }
// import React from "react";

// function Card({ title, description }) {
  return (
    <>
    <div style={styles.card}>
      <h3>test</h3>
      <p>description</p>
      <button>Read More</button>
    </div>
    <div style={styles.card}>
      <h3>test</h3>
      <p>description</p>
      <button>Read More</button>
    </div>
    </>
  );
}

const styles = {
  row: {
    display: "flex",
    gap: "20px",
  },
  card: {
    flex: 1,
    border: "1px solid #ccc",
    borderRadius: "8px",
    padding: "15px",
    boxShadow: "0 2px 5px rgba(0,0,0,0.1)",
  },
};


export default Dashboard;