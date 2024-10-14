import React, { createContext, useState, useContext } from 'react';


const DesignContext = createContext();

export const useDesignContext = () => useContext(DesignContext);

export const DesignProvider = ({ children }) => {
  const [designs, setDesigns] = useState([]);
  const [currentDesign, setCurrentDesign] = useState(null);

  const addDesign = (design) => {
    setDesigns(prevDesigns => {
      const newDesigns = [...prevDesigns, design];
      setCurrentDesign(design);  // 立即設置 currentDesign
      return newDesigns;
    });
  };

  const updateDesign = (updatedDesign) => {
    setDesigns(prevDesigns => {
      const newDesigns = prevDesigns.map(design => 
        design.designName === updatedDesign.designName ? updatedDesign : design
      );
      setCurrentDesign(updatedDesign);  // 立即設置 currentDesign
      return newDesigns;
    });
  };

  const selectDesign = (designName) => {
    const selected = designs.find(design => design.designName === designName);
    setCurrentDesign(selected);
  };

  const clearCurrentDesign = () => {
    setCurrentDesign(null);
  };

  return (
    <DesignContext.Provider value={{
      designs,
      currentDesign,
      addDesign,
      updateDesign,
      selectDesign,
      clearCurrentDesign,
    }}>
      {children}
    </DesignContext.Provider>
  );
};