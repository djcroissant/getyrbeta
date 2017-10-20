      var trip_member = TripMember.objects.get(pk=data.get('trip_member_id'));
      var email = trip_member.member.email;
      alert(trip_member + ' ' + email);
      if (trip_member.member.preferred_name) {
        var preferred_name = trip_member.member.preferred_name;
      }
      var pending_member = $('<div class="list-padding"><li class="trip-info">' + email + '</li>' + if(preferred_name){ '<li class="trip-info">' + preferred_name + '</li>' } +'</div>');
      $("#pending-members-list").find("ul").prepend(pending_member);
