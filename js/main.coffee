---
---

getVenueFromResult = (result) ->
  venue = ""
  if result.venue and result.venue.name
    venue = "Ort: #{result.venue.name}"
    latLng = [
      result.lat
      result.lon
    ]
  venue

setMeetupHtml = (result) ->
  $("#date span").html new Date(result.time).toLocaleDateString()
  $("#next-meetup #title").html result.name
  $("#next-meetup #venue").html getVenueFromResult(result)
  $("#next-meetup #description").html result.description
  $("#next-meetup #rvsp").attr "href", result.eventUrl

setMeetup = ->
  meetup_url = "https://api.meetup.com/2/events?callback=?&sign=true&status=upcoming&group_urlname=OK-Lab-Munster&format=json&key=48406a31956272b2f12c3965547d"
  $.getJSON meetup_url, (data) ->
    if data.results.length > 0
      result = data.results[0]
      setMeetupHtml(result)
    return

$(document).ready ->
  menuToggle = $("#js-mobile-menu").unbind()
  $("#js-navigation-menu").removeClass "show"
  menuToggle.on "click", (e) ->
    e.preventDefault()
    $("#js-navigation-menu").slideToggle ->
      $("#js-navigation-menu").removeAttr "style"  if $("#js-navigation-menu").is(":hidden")
      return
    return
  if $('#next-meetup').length > 0
    setMeetup()
    return
  return
