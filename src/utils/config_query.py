queries = {
    "Linear_Project": """
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
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
    """,
    "Linear_User": """
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
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
    """,
    "Linear_Issue": """
    query {
        issues({pagination}) {
            nodes {
                id
                title
                description
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
                creator { id name }
                assignee { id name }
                identifier
                url
                parent { id title }
            }
            pageInfo {
                hasNextPage
                endCursor
            }
        }
    }
    """
}

schemas = {
    "Linear_Project": (
        "id String `json:$.id`, "
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
    "Linear_User": (
        "id String `json:$.id`, "
        "name Nullable(String) `json:$.name`, "
        "displayName Nullable(String) `json:$.displayName`, "
        "initials Nullable(String) `json:$.initials`, "
        "email Nullable(String) `json:$.email`, "
        "guest Nullable(Bool) `json:$.guest`, "
        "active Nullable(Bool) `json:$.active`, "
        "admin Nullable(Bool) `json:$.admin`"
    ),
    "Linear_Issue": (
        "id String `json:$.id`, "
        "title Nullable(String) `json:$.title`, "
        "description Nullable(String) `json:$.description`, "
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
        "creator_name Nullable(String) `json:$.creator.name`, "
        "assignee_id Nullable(String) `json:$.assignee.id`, "
        "assignee_name Nullable(String) `json:$.assignee.name`, "
        "identifier Nullable(String) `json:$.identifier`, "
        "url Nullable(String) `json:$.url`, "
        "parent_id Nullable(String) `json:$.parent.id`, "
        "parentId Nullable(String) `json:$.parentId`, "
        "parentTitle Nullable(String) `json:$.parent.title`"
    )
}
