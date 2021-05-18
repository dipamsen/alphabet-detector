// const p5 = require("p5")

new p5((/** @type {import("p5")} */ p) => {
  document.querySelector(".clear").onclick = clear
  document.querySelector(".detect").onclick = detect
  const output = document.querySelector(".output")
  let currP = []
  let drawing = [currP]
  /** @type {import("p5").Image} */
  let img
  let g
  let cnv
  p.setup = () => {
    p.strokeJoin(p.ROUND)
    g = p.createGraphics(30, 22)
    g.strokeJoin(g.ROUND)
    cnv = p.createCanvas(600 / 2, 440 / 2)
    g.background('black')
    img = p.createImg(g.elt.toDataURL(), '')
    img.attribute('width', "300")
    img.attribute('height', "220")
  }
  p.draw = () => {
    p.background('black')
    p.stroke(255)
    p.strokeWeight(12)
    p.noFill()
    drawing.forEach(path => {
      p.beginShape()
      path.forEach(({ x, y }) => {
        p.vertex(x, y)
      })
      p.endShape()
    })
    g.image(cnv, 0, 0, 30, 22)
    img.attribute('src', g.elt.toDataURL())
  }
  p.mouseDragged = () => {
    currP.push({ x: p.mouseX, y: p.mouseY })
  }
  p.mouseReleased = () => {
    currP = []
    drawing.push(currP)
  }
  function clear() {
    currP = []
    drawing = [currP]
  }

  async function detect() {
    const res1 = await fetch(img.elt.src)
    const blob = await res1.blob()
    const fd = new FormData()
    fd.append("upl", blob)
    const res2 = await fetch('http://127.0.0.1:5000/predict', {
      method: "POST",
      body: fd
    })
    const response = await res2.text()
    console.log(response)
    const p = JSON.parse(response).pred[0]
    output.textContent = p
  }
}, "app")