from flask import Flask, jsonify
from repositories.xml_event_repository import XmlEventRepository
from services.event_service import EventService

app = Flask(__name__)

event_repository = XmlEventRepository(file_path="events.xml")
event_service = EventService(event_repository)


@app.route('/events')
def get_events():
    events = event_service.get_all_events()
    return jsonify([event.to_dict() for event in events])


if __name__ == '__main__':
    app.run()


# from repositories.xml_event_repository import XmlEventRepository
# from services.event_service import EventService
#
# event_repository = XmlEventRepository('events.xml')
# event_service = EventService(event_repository)
# events = event_service.get_all_events()
# for event in events:
#     print(event.name)
