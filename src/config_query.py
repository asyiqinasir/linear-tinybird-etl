queries = {
    "Linear_Projects": """
    query {
        projects {
            nodes {
                id
                name
                description
                health
                priority
                createdAt
                startDate
                targetDate
                updatedAt
                archivedAt
            }
        }
    }
    """,
    "Linear_Users": """
    query {
        users {
            nodes {
            id
            name
            displayName
            initials
            email
            guest
            active
            admin
            }
        }
    }
    """,
    "Linear_Issues": """
    query {
        issues {
            nodes {
                id
                title
                state { name }
                priority
                estimate
                createdAt
                updatedAt
                archivedAt
                startedAt
                completedAt
                canceledAt
                autoClosedAt
                autoArchivedAt
                dueDate
                trashed
                team {id name}
                cycle {id name}
                project {id name}
                projectMilestone {id name}
                creator {id displayName}
                assignee {id displayName}
                identifier
                url
                parent {id title}
                }
            }
        }
    """
}

schemas = {
    "Linear_Projects": (
        "id String `json:$.id`, "
        "name String `json:$.name`, "
        "createdAt DateTime64(3) `json:$.createdAt`, "
        "description String `json:$.description`, "
        "health Nullable(String) `json:$.health`, "
        "priority Int16 `json:$.priority`, "
        "startDate Nullable(Date) `json:$.startDate`, "
        "targetDate Nullable(Date) `json:$.targetDate`, "
        "updatedAt DateTime64(3) `json:$.updatedAt`"
    ),
    "Linear_Issues": (
        "id String `json:$.id`, "
        "title String `json:$.title`, "
        "state String `json:$.state.name`, "
        "priority Int16 `json:$.priority`, "
        "estimate Int16 `json:$.estimate`, "
        "createdAt DateTime64(3) `json:$.createdAt`, "
        "updatedAt DateTime64(3) `json:$.updatedAt`"
    )
}

