class HTMLNode:
  def __init__(self, tag: str = None, value: str = None, children: list["HTMLNode"] = None, props: dict[str, str] = None) -> None:
    self.tag = tag
    self.value = value
    self.children = children if children is not None else []
    self.props = props
    
  def to_html(self):
    raise NotImplementedError("to_html method not implemented")
  
  def props_to_html(self) -> str:
    if not self.props:
      return ""
    return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
        
  def __repr__(self) -> str:
    return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
  
  