
curl --request GET 'https://api.twitter.com/2/tweets?ids=1263145271946551300&expansions=attachments.media_keys&media.fields=duration_ms,height,media_key,preview_image_url,public_metrics,type,url,width,alt_text'
--header 'Authorization: Bearer $BEARER_TOKEN'