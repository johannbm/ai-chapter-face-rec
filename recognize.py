import face_recognition
from PIL import Image
import os
import glob
import utilities


def get_know_people_encodings(folder="objectnet-people/"):
    encodings = []
    names = []
    for filename in os.listdir(folder):
        if os.path.isfile(filename): continue
        try:
            image_path = glob.glob(folder + filename + "/" + '*600x750*')[0]
        except IndexError:
            print('{} has no 600x750 image'.format(filename))
            continue
        image = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(image)[0]
        encodings.append(face_encoding)
        names.append(filename)
        utilities.save_pickle_encodings(encodings, names)
    return encodings, names


def best_matches(known_face_encodings, face_encoding_to_check, tolerance=0.6):
    distances = face_recognition.face_distance(known_face_encodings, face_encoding_to_check)
    if distances.min(axis=0) > tolerance: return None
    return distances.argsort(axis=0)[:3]


if __name__ == "__main__":
    # Calculate encodings of known people. Saves to pickle
    # known_encodings, names = get_know_people_encodings()

    # Load our encodings from pickle on subsequent runs
    known_encodings, names = utilities.load_pickle_encodings()

    # Load the image of people we want to identify
    img_to_identify = face_recognition.load_image_file("knowit.jpg")

    # Find the face regions of people in the image
    face_locations = face_recognition.face_locations(img_to_identify)

    # Use those face regions to calculate the encoding of our unknown faces
    unknown_encodings = face_recognition.face_encodings(img_to_identify, face_locations)

    # Make a copy of our image so that PIL can draw on it
    pil_image = Image.fromarray(img_to_identify)

    # Draw all the found faces
    for location in face_locations:
        utilities.draw_rect(pil_image, location, color=(0, 255, 0))

    # Loop through each encoding of our unknown faces. Find the closest match(es)
    best_matches = [(face_locations[j], [best_matches(known_encodings, unknown_encodings[j])]) for j in range(len(unknown_encodings))]
    for location, matches in best_matches:
        if matches[0] is None: continue
        matched_names = [names[match] for match in matches[0]]
        utilities.draw_name(pil_image, location, matched_names)

    pil_image.show()
