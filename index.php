<?php
$json = file_get_contents("src/data.json");
$data = json_encode($json,true);
?>

<!doctype html>
<html>
    <head>
        <title>Animedley</title>
        <link rel="stylesheet" type="text/css" href="assets/style.css">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
        <script src="assets/main.js"></script>
        <script>
            const json = <?php echo $data ?>;
            const data = JSON.parse(json);
            const r_data = listrandom(data);
        </script>
    </head>
    <!--<NOSCRIPT><body></NOSCRIPT>-->
    <body>
        <div><img id="illust" src="img/dummy.jpg" width="300" height="300"></div>
        <div class="progress_bar"><progress id="progress" value="" max=""></progress></div>
        <div class="title">
            <p class="title"><span id="title"></span></p>
        </div>
        <div class="main_info">
            <div class="st">
                <p class="main_text"><span class="set">feat</span></p>
                <p class="main_text"><span class="set">artist</span></p>
                <p class="main_text"><span class="set">release</span></p>
                <p class="main_text"><span class="set">genre</span></p>
            </div>
            <div class="ot">
                <p class="main_text"><span id="feat"></span></p>
                <p class="main_text"><span id="artist"></span></p>
                <p class="main_text"><span id="release"></span></p>
                <p class="main_text"><span id="genre"></span></p>
            </div>
        </div>
    </body>
    <script>
        var count = -1;
        var playsoundstatus = false;
        function mp3player(){
            playsoundstatus = true;
            count++
            if(count < r_data.length){
                document.getElementById("illust").setAttribute('src', "music/illust/"+r_data[count]["file_data"]["illust_path"]);
                document.getElementById("title").innerHTML = r_data[count]["music_data"]["name"];
                document.getElementById("feat").innerHTML = r_data[count]["music_data"]["featuring"];
                document.getElementById("artist").innerHTML = r_data[count]["music_data"]["artist_name"];
                document.getElementById("release").innerHTML = r_data[count]["music_data"]["release_date"];
                document.getElementById("genre").innerHTML = r_data[count]["music_data"]["genre"];
                var audio = new Audio();
                audio.src = "music/mp3/"+r_data[count]["file_data"]["mp3_path"]; // 音声ファイルを指定
                audio.load(); // 読み込み
                audio.volume = 0;
                console.log("load audio");
                audio.addEventListener('loadedmetadata',function(){
                    audio.play();
                    var endTime = audio.duration;

                    // プログレスバー
                    document.getElementById("progress").max = endTime;
                    function updateProgress(){
                        let Time = audio.currentTime;
                        document.getElementById("progress").value = Time;
                    }
                    var progress = setInterval(updateProgress, 100);
                    
                    // フェードイン
                    function volumeup(){
                        if(audio.volume==0.5){
                            clearInterval(volumeupInterval);
                        }else{
                            audio.volume = audio.volume + 0.1; 
                        }
                    }
                    var volumeupInterval = setInterval(volumeup, 200);

                    // フェードアウト
                    function observar(){
                        if(audio.currentTime>=endTime-1){
                            function volumedown(){
                                if(Math.round(audio.volume*10)/10==0){
                                    clearInterval(volumedownInterval);
                                }else{
                                    audio.volume = audio.volume - 0.1; 
                                }
                            }
                            clearInterval(observarInterval);
                            var volumedownInterval = setInterval(volumedown, 200);
                        }
                    }
                    var observarInterval = setInterval(observar, 100);
                    audio.addEventListener('ended', function(){
                        clearInterval(progress); // プログレスバー終了
                        console.log("end audio");
                        mp3player(); // 終了まで待機して次を再生
                    }, false);
                }, false); // 再生
            }
        }
        document.getElementById('illust').addEventListener('click', function() {
            // 開始
            if(!playsoundstatus){
                mp3player();
            }
        }, false);
    </script>
</html>