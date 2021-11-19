import face_recognition
import cv2
import numpy as np


def recognize_face(users: list):
    # Pegas a referência da camera padrão do sistema
    try:
        video_capture = cv2.VideoCapture(0)
    except:
        return "Erro: não foi possível instanciar a camera"

    # Cria uma lista que guardará os rostos/nomes conhecidos
    known_face_encodings = []
    known_face_names = []

    # Carrega as imagens dos usuários (e seus nomes em suas respectivas imagens)
    for user in users:
        user_image = face_recognition.load_image_file(user.imagepath)
        user_image = face_recognition.face_encodings(user_image)[0]

        # Create arrays of known face encodings and their names
        known_face_encodings.append(user_image)
        known_face_names.append(user.name)

    if not known_face_encodings:
        return 'ERRO: NÃO EXISTEM USUÁRIOS CADASTRADOS'

    # Initialize some variables
    face_locations = []
    face_names = []
    process_this_frame = True

    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()

        # Redimensiona o frame para 1/4 da resolução para processar a imagem mais rapidamente
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Converte a imagem da cor BGR (que o OpenCV usa) para a cor RGB (que o face_recognition usa)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Só processa um em cada 2 frames (um sim, um não)
        if process_this_frame:
            # Coleta todos os rostos presentes no frame capturado
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
                # Vê se algum dos rostos é conhecido (salvo no banco)
                matches = face_recognition.compare_faces(known_face_encodings,  face_encoding)

                # Define um nome padrão para os rostos
                user = "Desconhecido"

                # Usa o rosto conhecido com a menor distância para o novo rosto
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    user = known_face_names[best_match_index]

                    # Libera a webcam para o sistema
                    video_capture.release()
                    cv2.destroyAllWindows()

                    return user

                face_names.append(user)

        process_this_frame = not process_this_frame

        # Mostra o resultado para os rostos encontrados (não conhecidos)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Multiplica os valores por 4 para retornar a resolução padrão (pois dividimos por 4 anteriomente)
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Desenha um quadrado em volta do rosto
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Escreve o nome
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

        # Mostra o frame
        cv2.imshow('Video capturado', frame)

        # Seta o botão "Q" para finalizar a função.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Caso a função seja finalizada, libera a camera para o sitema
    video_capture.release()
    cv2.destroyAllWindows()
