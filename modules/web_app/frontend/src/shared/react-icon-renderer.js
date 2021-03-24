import { IconContext } from "react-icons"

const ReactIconRender = (props) => {
  const { IconComponent, color, className } = props
  return (
    <IconContext.Provider value={{ color: color, className: className }}>
      <IconComponent />
    </IconContext.Provider>
  )
}

export default ReactIconRender