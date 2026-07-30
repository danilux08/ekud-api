def get_player_html(videoId: str):
    return f"""<!DOCTYPE html>
        <html>
            <head>
                <meta name="referrer" content="strict-origin-when-cross-origin" />
                <style>
                    body {{
                        margin: 0;
                    }}
                    #player {{
                        width: 100%;
                    }}
                </style>
            </head>
            <body>
                <div id="player"></div>
                <script>
                    let tag = document.createElement("script");
                    tag.src = "https://www.youtube.com/iframe_api";
                    let firstScriptTag = document.getElementsByTagName("script")[0];
                    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
                    let player;
                    function onYouTubeIframeAPIReady() {{
                        player = new YT.Player("player", {{
                            videoId: "{videoId}",
                            playerVars: {{
                                playsinline: 1,
                                controls: 0
                            }},
                            events: {{
                                onStateChange: onPlayerStateChange,
                            }},
                        }});
                    }}
                    let done = false;
                    function onPlayerStateChange(event) {{
                        if (event.data == YT.PlayerState.PLAYING && !done) {{
                            setTimeout(stopVideo, 6000);
                            done = true;
                        }}
                    }}
                    function stopVideo() {{
                        player.stopVideo();
                    }}
                </script>
            </body>
    </html>"""
