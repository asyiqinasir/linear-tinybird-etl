queries = {
    "Linear_Projects": """
    query {
        projects({pagination}) {
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
        users({pagination}) {
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
        issues({pagination}) {
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
                team { id name }
                cycle { id name }
                project { id name }
                projectMilestone { id name }
                creator { id displayName }
                assignee { id displayName }
                identifier
                url
                parent { id title }
            }
        }
    }
    """
}

schemas = {
    "Linear_Projects": (
        "id Nullable(String) `json:$.id`, "
        "name Nullable(String) `json:$.name`, "
        "description Nullable(String) `json:$.description`, "
        "health Nullable(String) `json:$.health`, "
        "priority Nullable(Int16) `json:$.priority`, "
        "createdAt Nullable(DateTime64(3)) `json:$.createdAt`, "
        "startDate Nullable(Date) `json:$.startDate`, "
        "targetDate Nullable(Date) `json:$.targetDate`, "
        "updatedAt Nullable(DateTime64(3)) `json:$.updatedAt`, "
        "archivedAt Nullable(DateTime64(3)) `json:$.archivedAt`"
    ),
    "Linear_Users": (
        "id Nullable(String) `json:$.id`, "
        "name Nullable(String) `json:$.name`, "
        "displayName Nullable(String) `json:$.displayName`, "
        "initials Nullable(String) `json:$.initials`, "
        "email Nullable(String) `json:$.email`, "
        "guest Nullable(Bool) `json:$.guest`, "
        "active Nullable(Bool) `json:$.active`, "
        "admin Nullable(Bool) `json:$.admin`"
    ),
    "Linear_Issues": (
        "id Nullable(String) `json:$.id`, "
        "title Nullable(String) `json:$.title`, "
        "state Nullable(String) `json:$.state.name`, "
        "priority Nullable(Int16) `json:$.priority`, "
        "estimate Nullable(Int16) `json:$.estimate`, "
        "createdAt Nullable(DateTime64(3)) `json:$.createdAt`, "
        "updatedAt Nullable(DateTime64(3)) `json:$.updatedAt`, "
        "archivedAt Nullable(DateTime64(3)) `json:$.archivedAt`, "
        "startedAt Nullable(DateTime64(3)) `json:$.startedAt`, "
        "completedAt Nullable(DateTime64(3)) `json:$.completedAt`, "
        "canceledAt Nullable(DateTime64(3)) `json:$.canceledAt`, "
        "autoClosedAt Nullable(DateTime64(3)) `json:$.autoClosedAt`, "
        "autoArchivedAt Nullable(DateTime64(3)) `json:$.autoArchivedAt`, "
        "dueDate Nullable(Date) `json:$.dueDate`, "
        "trashed Nullable(Bool) `json:$.trashed`, "
        "team_id Nullable(String) `json:$.team.id`, "
        "team_name Nullable(String) `json:$.team.name`, "
        "cycle_id Nullable(String) `json:$.cycle.id`, "
        "cycle_name Nullable(String) `json:$.cycle.name`, "
        "project_id Nullable(String) `json:$.project.id`, "
        "project_name Nullable(String) `json:$.project.name`, "
        "milestone_id Nullable(String) `json:$.projectMilestone.id`, "
        "milestone_name Nullable(String) `json:$.projectMilestone.name`, "
        "creator_id Nullable(String) `json:$.creator.id`, "
        "creator_name Nullable(String) `json:$.creator.displayName`, "
        "assignee_id Nullable(String) `json:$.assignee.id`, "
        "assignee_name Nullable(String) `json:$.assignee.displayName`, "
        "identifier Nullable(String) `json:$.identifier`, "
        "url Nullable(String) `json:$.url`, "
        "parent_id Nullable(String) `json:$.parent.id`, "
        "parent_title Nullable(String) `json:$.parent.title`"
    )
}
