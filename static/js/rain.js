function do_rain(src_image)
{
    duration = 3000;
    end = Date.now() + duration;

    interval = setInterval(() =>
    {

        img = document.createElement("img");
        img.src = src_image;
        img.className = "rain-img";
        img.style.left = Math.random() * window.innerWidth + "px";
        img.style.animationDuration = (Math.random() * 2 + 2) + "s";

        document.body.appendChild(img);

        setTimeout(() => img.remove(), 4000);
    }, 100);
}