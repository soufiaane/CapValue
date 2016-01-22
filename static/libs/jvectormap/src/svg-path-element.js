<<<<<<< HEAD
jvm.SVGPathElement = function(config, style){
  jvm.SVGPathElement.parentClass.call(this, 'path', config, style);
  this.node.setAttribute('fill-rule', 'evenodd');
}

=======
jvm.SVGPathElement = function(config, style){
  jvm.SVGPathElement.parentClass.call(this, 'path', config, style);
  this.node.setAttribute('fill-rule', 'evenodd');
}

>>>>>>> 942286391f24f61d690faaf4c33948109167ed24
jvm.inherits(jvm.SVGPathElement, jvm.SVGShapeElement);