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
  
class LeafNode(HTMLNode):
  def __init__(self, tag: str = None, value: str = None, props: dict[str, str] = None) -> None:
    super().__init__(tag=tag, value=value, children=None, props=props)
    
  def to_html(self):
    if self.value is None:
      raise ValueError("Invalid HTML: LeafNode must have a value")
    
    if self.tag is None:
      return self.value
  
    return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
  
  def props_to_html(self) -> str:
    if not self.props:
      return ""
    return " " + " ".join(f'{key}="{value}"' for key, value in self.props.items())
        
  def __repr__(self) -> str:
    return f"LeafNode({self.tag}, {self.value}, {self.props})"
  
class ParentNode(HTMLNode):
  def __init__(self, tag: str, children: list[HTMLNode], props: dict[str, str] = None) -> None:
        super().__init__(tag=tag, value=None, children=children, props=props)

  def to_html(self) -> str:
      if self.tag is None:
            raise ValueError("Invalid HTML: ParentNode must have a tag")
      if not self.children:
            raise ValueError("Invalid HTML: ParentNode must have children")


      children_html = "".join(child.to_html() for child in self.children)
        
      return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"