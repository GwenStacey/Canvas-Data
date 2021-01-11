def get_quizzes(course_id, headers):
    """This function returns a list of JSONs
    that include all of the quizzes for a given course
    The main purpose for this function is to find the
    peer mentorship review quizzes we give the students
    but this would return useful data about any quizzes
    we were interested in.
    USAGE:
    This function requires that you have an API predefined.
    Most users won't notice this in the front end as we'll
    build the key into the program. If you're servicing in the
    future headers should look like:
    headers = {"Authorization":f"Bearer {api_key}"}
    jsons = get_quizes(400, headers)
    """
    r = requests.get(f"https://lambdaschool.instructure.com/api/v1/courses/{course_id}/quizzes", headers=headers)
    raw = r.json()
    for i in raw:
        i["course_id"] = course_id
    return raw


def get_submissions(course_id, quiz_id, headers):
    """Creates a small list of jsons
    that can be made into a file very easily
    then converted to a dataframe for exploration
    This particular design is just for grabbing pagniated
    information from the api and returning it in a useful
    way.
    Usage:
    This function requires that you have an API predefined.
    Most users won't notice this in the front end as we'll
    build the key into the program. If you're servicing in the
    future headers should look like:
    headers = {"Authorization":f"Bearer {api_key}"}
    Example ids used, not real
    jsons = get_submissions(400, 1000)
    with open("some_json_title.json", "w") as outfile:
        json.dump(data_set, outfile)
    """
    r = requests.get(f"https://lambdaschool.instructure.com/api/v1/courses/{course_id}/quizzes/{quiz_id}/submissions", headers=headers)
    data_set = []
    raw = r.json()

    for submission in raw["quiz_submissions"]:
        submission["course_id"] = course_id
        submission["quiz_id"] = quiz_id
        data_set.append(submission)

    if "next" in r.links.keys():
        while "next" in r.links.keys():
            r = requests.get(r.links["next"]["url"], headers=headers)
            raw = r.json()
            for submission in raw["quiz_submissions"]:
                submission["course_id"] = course_id
                submission["quiz_id"] = quiz_id
                data_set.append(submission)
        if "last" in r.links.keys() and r.links['current']['url'] == r.links['last']['url']:
            print('Done!')
    else:
        print("Just one page!")
    return data_set