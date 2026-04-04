-- Unimos primero los eventos de uso (Silver) para consolidar las métricas por día y usuario
FROM {{ ref('stg_calls') }} AS c

FULL OUTER JOIN {{ ref('stg_messages') }} AS m
    ON c.user_id = m.user_id 
    AND c.call_date = m.message_date

FULL OUTER JOIN {{ ref('stg_internet') }} AS i
    ON COALESCE(c.user_id, m.user_id) = i.user_id 
    AND COALESCE(c.call_date, m.message_date) = i.session_date

-- Cruzamos con la dimensión de usuarios (Source)
LEFT JOIN {{ source('megaline', 'users') }} AS u
    ON COALESCE(c.user_id, m.user_id, i.user_id) = u.user_id

-- Cruzamos con la dimensión de planes (Source) a través de la tabla de usuarios
LEFT JOIN {{ source('megaline', 'plans') }} AS p
    ON u.plan = p.plan_name