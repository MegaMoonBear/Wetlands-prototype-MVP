//  JSX for header section of index.html, which includes the title and introductory text for the Wetlands MVP project. This component is designed to be simple and informative, providing users with a clear understanding of the purpose of the site and encouraging them to participate by sharing photos of water or wetlands in their neighborhoods. The header sets the tone for the user experience, emphasizing the importance of community involvement in supporting water resources.

import React from 'react';

export default function Header() {
  return (
    <header style={styles.header}>
      <h1>My App</h1>
    </header>
  );
}

// See .css or index.html file for these styles, which are not currently used in the header but may be applied to other components or elements in the app
// const styles = {
//   header: {
//     padding: "1rem",
//     backgroundColor: "#1e293b",
//     color: "white",
//   },
// };