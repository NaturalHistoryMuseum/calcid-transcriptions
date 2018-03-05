<template>
    <div id="image-viewer-wrapper">
        <canvas @mouseup="onMouseUp" @mousedown="onMouseDown" @mousemove="onMouseMove" @DOMMouseScroll="onScrollZoom" @mousewheel="onScrollZoom"></canvas>
        <button @click="onRotateLeft" class="btn btn-control"><icon name="rotate-left"></icon></button>
        <button @click="onRotateRight" class="btn btn-control"><icon name="rotate-right"></icon></button>
        <button @click="onZoomOut" class="btn btn-control"><icon name="search-minus"></icon></button>
        <button @click="onZoomIn" class="btn btn-control"><icon name="search-plus"></icon></button>
    </div>
</template>

<script>
    export default {
        props: ['url'],
          watch : {
            url : function () {
              console.log('URL Changed');
              this.resetAllTransformations();
              this.updateImage();
            }
        },
        data () {
            return {
                canvas: null,
                ctx: null,
                image: new Image,
                scaleFactor: 1.2,
                dragStart: null,
                dragged: null
            }
        },
        created: function () {
            window.addEventListener('keyup', this.onKeyUp)
            this.updateImage();
        },
        computed: {
            // a computed getter
            lastX: function () {
                return this.canvas.width / 2
            },
            lastY: function () {
                return this.canvas.height / 2
            }
        },
        mounted: function () {
            this.canvas = this.$el.getElementsByTagName('canvas')[0];
            // Set the canvas to the parent element width / height
            this.canvas.width = this.$el.clientWidth;
            this.canvas.height = this.$el.clientHeight;
            this.ctx = this.canvas.getContext('2d');
            this.trackTransforms();
        },
        // define methods under the `methods` object
        methods: {
            updateImage: function(){
                if(this.url){
                    this.image.src = this.url;
                    this.image.onload = function () {
                        this.$emit('imageLoaded');
                        this.redraw();
                    }.bind(this);
                }
            },
            resetAllTransformations: function(){
              this.ctx.setTransform(1, 0, 0, 1, 0, 0);
            },
            redraw: function () {
                // Clear the entire canvas
                let p1 = this.ctx.transformedPoint(0, 0);
                let p2 = this.ctx.transformedPoint(this.canvas.width, this.canvas.height);
                this.ctx.clearRect(p1.x, p1.y, p2.x - p1.x, p2.y - p1.y);
                this.ctx.save();
                this.resetAllTransformations();
                this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
                this.ctx.restore();
                let w, h, xCenter = 0, yCenter = 0;
                // If image is wider than high, ensure it fits width-wise
                // Otherwise, ensure it fits by height
                if (this.image.width > this.image.height) {
                    w = this.canvas.width;
                    h = this.image.height / (this.image.width / this.canvas.width);
                    xCenter = (this.canvas.height / 2) - (h / 2);
                } else {
                    h = this.canvas.height;
                    w = this.image.width / (this.image.height / this.canvas.height);
                    yCenter = (this.canvas.width / 2) - (w / 2);
                }
                this.ctx.drawImage(this.image, yCenter, xCenter, w, h);
            },
            trackTransforms: function () {
                let svg = document.createElementNS("http://www.w3.org/2000/svg", 'svg');
                let xform = svg.createSVGMatrix();
                this.ctx.getTransform = function () {
                    return xform;
                };
                let savedTransforms = [];
                let save = this.ctx.save;
                this.ctx.save = function () {
                    savedTransforms.push(xform.translate(0, 0));
                    return save.call(this.ctx);
                }.bind(this);
                let restore = this.ctx.restore;
                this.ctx.restore = function () {
                    xform = savedTransforms.pop();
                    return restore.call(this.ctx);
                }.bind(this);
                let scale = this.ctx.scale;
                this.ctx.scale = function (sx, sy) {
                    xform = xform.scaleNonUniform(sx, sy);
                    return scale.call(this.ctx, sx, sy);
                }.bind(this);
                let rotate = this.ctx.rotate;
                this.ctx.rotate = function (radians) {
                    xform = xform.rotate(radians * 180 / Math.PI);
                    return rotate.call(this.ctx, radians);
                }.bind(this);
                let translate = this.ctx.translate;
                this.ctx.translate = function (dx, dy) {
                    xform = xform.translate(dx, dy);
                    return translate.call(this.ctx, dx, dy);
                }.bind(this);
                let transform = this.ctx.transform;
                this.ctx.transform = function (a, b, c, d, e, f) {
                    let m2 = svg.createSVGMatrix();
                    m2.a = a;
                    m2.b = b;
                    m2.c = c;
                    m2.d = d;
                    m2.e = e;
                    m2.f = f;
                    xform = xform.multiply(m2);
                    return transform.call(this.ctx, a, b, c, d, e, f);
                }.bind(this);
                let setTransform = this.ctx.setTransform;
                this.ctx.setTransform = function (a, b, c, d, e, f) {
                    xform.a = a;
                    xform.b = b;
                    xform.c = c;
                    xform.d = d;
                    xform.e = e;
                    xform.f = f;
                    return setTransform.call(this.ctx, a, b, c, d, e, f);
                }.bind(this);
                let pt = svg.createSVGPoint();
                this.ctx.transformedPoint = function (x, y) {
                    pt.x = x;
                    pt.y = y;
                    return pt.matrixTransform(xform.inverse());
                }
            },
            zoom: function (clicks) {
                let pt = this.ctx.transformedPoint(this.lastX, this.lastY);
                this.ctx.translate(pt.x, pt.y);
                let factor = Math.pow(this.scaleFactor, clicks);
                this.ctx.scale(factor, factor);
                this.ctx.translate(-pt.x, -pt.y);
                this.redraw();
            },
            rotate: function (direction) {
                // 90 degrees in radians * 1/-1
                let r = direction * 1.5708;
                let pt = this.ctx.transformedPoint(this.lastX, this.lastY);
                this.ctx.translate(pt.x, pt.y);
                this.ctx.rotate(r);
                this.ctx.translate(-pt.x, -pt.y);
                this.redraw();
            },
            // Event handlers
            onScrollZoom: function (e) {
                let delta = e.wheelDelta ? e.wheelDelta / 40 : e.detail ? -e.detail : 0;
                if (delta) this.zoom(delta);
                return e.preventDefault() && false;
            },
            onMouseUp: function (e) {
                this.dragStart = null;
                if (!this.dragged) this.zoom(e.shiftKey ? -1 : 1);
            },
            onMouseDown: function (e) {
              document.body.style.mozUserSelect = document.body.style.webkitUserSelect = document.body.style.userSelect = 'none';
              let lastX = e.offsetX || (e.pageX - this.canvas.offsetLeft);
              let lastY = e.offsetY || (e.pageY - this.canvas.offsetTop);
              this.dragStart = this.ctx.transformedPoint(lastX,lastY);
              this.dragged = false;
            },
            onMouseMove: function (e) {
              let lastX = e.offsetX || (e.pageX - this.canvas.offsetLeft);
              let lastY = e.offsetY || (e.pageY - this.canvas.offsetTop);
              this.dragged = true;
              if(this.dragStart){
                let pt = this.ctx.transformedPoint(lastX,lastY);
                this.ctx.translate(pt.x-this.dragStart.x,pt.y-this.dragStart.y);
                this.redraw();
              }
            },
            onRotateLeft: function () {
                this.rotate(-1)
            },
            onRotateRight: function () {
                this.rotate(1)
            },
            onZoomIn: function () {
                this.zoom(1);
            },
            onZoomOut: function () {
                this.zoom(-1);
            },
            onKeyUp: function(e){
             if(e.key == 'ArrowLeft' || e.keyCode == 37){
                this.rotate(-1)
             }else if(e.key == 'ArrowRight' || e.keyCode == 39){
                this.rotate(1)
             }
            }
        }
    }
</script>

<style lang="scss">
    $button-space: 34px;
    $button-offset: 7px;
    #image-viewer-wrapper {
        height: 100%;
        position: relative;
        button{
            position: absolute;
            top: $button-offset;
            left: $button-offset;
            &:nth-child(3){
                left: $button-space + $button-offset;
             }
            &:nth-child(4){
                left: ($button-space * 2) + $button-offset;
             }
            &:nth-child(5){
                left: ($button-space * 3) + $button-offset;
             }
        }
    }
</style>