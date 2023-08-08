# Header styling
header = """<style>

.header {
    position: fixed;
    left: 0;
    top: 0;
    color: black;
    text-align: center;
    height: 30%;
    width: 100%;
}

#myVideo {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.overlay {
    top: 13.5vh;
    left: 37vw;
    position:absolute;
    z-index:1;
}

</style>

<div class="header">
    <video playsinline autoplay muted loop id="myVideo">
        <source src="https://www.lgs.com/content/dam/lgsaem/home/home%20bg%20video%20optimized.mp4")>
    </video>
    <div class="overlay">
            <h1 style="color:White;">PolyBM Data Analysis Tool</h1>
    </div>
</div>

<br></br>
<br></br>
<br></br>
"""