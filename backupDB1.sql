--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: administrarFases_fase; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarFases_fase" (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    estado character varying(3) NOT NULL,
    proyecto_id integer NOT NULL,
    nro_orden integer NOT NULL
);


ALTER TABLE public."administrarFases_fase" OWNER TO zar;

--
-- Name: administrarFases_fase_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarFases_fase_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarFases_fase_id_seq" OWNER TO zar;

--
-- Name: administrarFases_fase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarFases_fase_id_seq" OWNED BY "administrarFases_fase".id;


--
-- Name: administrarItems_campofile; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarItems_campofile" (
    id integer NOT NULL,
    item_id integer NOT NULL,
    atributo_id integer NOT NULL,
    archivo character varying(100) NOT NULL
);


ALTER TABLE public."administrarItems_campofile" OWNER TO zar;

--
-- Name: administrarItems_campofile_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarItems_campofile_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarItems_campofile_id_seq" OWNER TO zar;

--
-- Name: administrarItems_campofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarItems_campofile_id_seq" OWNED BY "administrarItems_campofile".id;


--
-- Name: administrarItems_campoimagen; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarItems_campoimagen" (
    id integer NOT NULL,
    item_id integer NOT NULL,
    atributo_id integer NOT NULL,
    imagen character varying(100) NOT NULL
);


ALTER TABLE public."administrarItems_campoimagen" OWNER TO zar;

--
-- Name: administrarItems_campoimagen_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarItems_campoimagen_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarItems_campoimagen_id_seq" OWNER TO zar;

--
-- Name: administrarItems_campoimagen_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarItems_campoimagen_id_seq" OWNED BY "administrarItems_campoimagen".id;


--
-- Name: administrarItems_camponumero; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarItems_camponumero" (
    id integer NOT NULL,
    item_id integer NOT NULL,
    atributo_id integer NOT NULL,
    valor double precision NOT NULL
);


ALTER TABLE public."administrarItems_camponumero" OWNER TO zar;

--
-- Name: administrarItems_camponumero_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarItems_camponumero_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarItems_camponumero_id_seq" OWNER TO zar;

--
-- Name: administrarItems_camponumero_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarItems_camponumero_id_seq" OWNED BY "administrarItems_camponumero".id;


--
-- Name: administrarItems_campotextocorto; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarItems_campotextocorto" (
    id integer NOT NULL,
    item_id integer NOT NULL,
    atributo_id integer NOT NULL,
    valor character varying(140) NOT NULL
);


ALTER TABLE public."administrarItems_campotextocorto" OWNER TO zar;

--
-- Name: administrarItems_campotextocorto_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarItems_campotextocorto_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarItems_campotextocorto_id_seq" OWNER TO zar;

--
-- Name: administrarItems_campotextocorto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarItems_campotextocorto_id_seq" OWNED BY "administrarItems_campotextocorto".id;


--
-- Name: administrarItems_campotextolargo; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarItems_campotextolargo" (
    id integer NOT NULL,
    item_id integer NOT NULL,
    atributo_id integer NOT NULL,
    valor character varying(900) NOT NULL
);


ALTER TABLE public."administrarItems_campotextolargo" OWNER TO zar;

--
-- Name: administrarItems_campotextolargo_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarItems_campotextolargo_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarItems_campotextolargo_id_seq" OWNER TO zar;

--
-- Name: administrarItems_campotextolargo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarItems_campotextolargo_id_seq" OWNED BY "administrarItems_campotextolargo".id;


--
-- Name: administrarItems_itembase; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarItems_itembase" (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    usuario_modificacion_id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    descripcion text,
    estado character varying(3) NOT NULL,
    fecha_creacion timestamp with time zone,
    fecha_modificacion timestamp with time zone,
    tipoitem_id integer NOT NULL,
    complejidad integer NOT NULL,
    costo integer NOT NULL,
    tiempo integer NOT NULL,
    version integer NOT NULL,
    linea_base_id integer
);


ALTER TABLE public."administrarItems_itembase" OWNER TO zar;

--
-- Name: administrarItems_itembase_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarItems_itembase_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarItems_itembase_id_seq" OWNER TO zar;

--
-- Name: administrarItems_itembase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarItems_itembase_id_seq" OWNED BY "administrarItems_itembase".id;


--
-- Name: administrarItems_itembase_solicitudes; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarItems_itembase_solicitudes" (
    id integer NOT NULL,
    itembase_id integer NOT NULL,
    solicitudcambios_id integer NOT NULL
);


ALTER TABLE public."administrarItems_itembase_solicitudes" OWNER TO zar;

--
-- Name: administrarItems_itembase_solicitudes_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarItems_itembase_solicitudes_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarItems_itembase_solicitudes_id_seq" OWNER TO zar;

--
-- Name: administrarItems_itembase_solicitudes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarItems_itembase_solicitudes_id_seq" OWNED BY "administrarItems_itembase_solicitudes".id;


--
-- Name: administrarItems_itemrelacion; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarItems_itemrelacion" (
    id integer NOT NULL,
    "itemPadre_id" integer,
    "itemHijo_id" integer NOT NULL,
    estado character varying(3) NOT NULL
);


ALTER TABLE public."administrarItems_itemrelacion" OWNER TO zar;

--
-- Name: administrarItems_itemrelacion_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarItems_itemrelacion_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarItems_itemrelacion_id_seq" OWNER TO zar;

--
-- Name: administrarItems_itemrelacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarItems_itemrelacion_id_seq" OWNED BY "administrarItems_itemrelacion".id;


--
-- Name: administrarLineaBase_lineabase; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarLineaBase_lineabase" (
    id integer NOT NULL,
    fase_id integer NOT NULL,
    fecha_creacion date,
    fecha_modificacion date,
    observaciones text
);


ALTER TABLE public."administrarLineaBase_lineabase" OWNER TO zar;

--
-- Name: administrarLineaBase_lineabase_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarLineaBase_lineabase_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarLineaBase_lineabase_id_seq" OWNER TO zar;

--
-- Name: administrarLineaBase_lineabase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarLineaBase_lineabase_id_seq" OWNED BY "administrarLineaBase_lineabase".id;


--
-- Name: administrarLineaBase_solicitudcambios; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarLineaBase_solicitudcambios" (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    fase_id integer NOT NULL,
    motivo text NOT NULL,
    fecha_creacion timestamp with time zone,
    estado character varying(3) NOT NULL,
    costo integer NOT NULL,
    tiempo integer NOT NULL
);


ALTER TABLE public."administrarLineaBase_solicitudcambios" OWNER TO zar;

--
-- Name: administrarLineaBase_solicitudcambios_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarLineaBase_solicitudcambios_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarLineaBase_solicitudcambios_id_seq" OWNER TO zar;

--
-- Name: administrarLineaBase_solicitudcambios_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarLineaBase_solicitudcambios_id_seq" OWNED BY "administrarLineaBase_solicitudcambios".id;


--
-- Name: administrarLineaBase_votacion; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarLineaBase_votacion" (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    solicitud_id integer NOT NULL,
    voto character varying(4) NOT NULL,
    justificacion text NOT NULL
);


ALTER TABLE public."administrarLineaBase_votacion" OWNER TO zar;

--
-- Name: administrarLineaBase_votacion_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarLineaBase_votacion_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarLineaBase_votacion_id_seq" OWNER TO zar;

--
-- Name: administrarLineaBase_votacion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarLineaBase_votacion_id_seq" OWNED BY "administrarLineaBase_votacion".id;


--
-- Name: administrarProyectos_proyecto; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarProyectos_proyecto" (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    lider_proyecto_id integer NOT NULL,
    descripcion text,
    fecha_creacion date,
    fecha_inicio date,
    fecha_fin date,
    estado character varying(3) NOT NULL,
    observaciones text
);


ALTER TABLE public."administrarProyectos_proyecto" OWNER TO zar;

--
-- Name: administrarProyectos_proyecto_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarProyectos_proyecto_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarProyectos_proyecto_id_seq" OWNER TO zar;

--
-- Name: administrarProyectos_proyecto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarProyectos_proyecto_id_seq" OWNED BY "administrarProyectos_proyecto".id;


--
-- Name: administrarProyectos_usuariosvinculadosproyectos; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarProyectos_usuariosvinculadosproyectos" (
    id integer NOT NULL,
    cod_proyecto_id integer NOT NULL,
    cod_usuario_id integer NOT NULL,
    habilitado boolean NOT NULL
);


ALTER TABLE public."administrarProyectos_usuariosvinculadosproyectos" OWNER TO zar;

--
-- Name: administrarProyectos_usuariosvinculadosproyectos_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarProyectos_usuariosvinculadosproyectos_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarProyectos_usuariosvinculadosproyectos_id_seq" OWNER TO zar;

--
-- Name: administrarProyectos_usuariosvinculadosproyectos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarProyectos_usuariosvinculadosproyectos_id_seq" OWNED BY "administrarProyectos_usuariosvinculadosproyectos".id;


--
-- Name: administrarRolesPermisos_permiso; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarRolesPermisos_permiso" (
    id integer NOT NULL,
    code character varying(20) NOT NULL,
    nombre character varying(50) NOT NULL,
    descripcion character varying(100) NOT NULL
);


ALTER TABLE public."administrarRolesPermisos_permiso" OWNER TO zar;

--
-- Name: administrarRolesPermisos_permiso_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarRolesPermisos_permiso_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarRolesPermisos_permiso_id_seq" OWNER TO zar;

--
-- Name: administrarRolesPermisos_permiso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarRolesPermisos_permiso_id_seq" OWNED BY "administrarRolesPermisos_permiso".id;


--
-- Name: administrarRolesPermisos_rol; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarRolesPermisos_rol" (
    id integer NOT NULL,
    grupo_id integer NOT NULL,
    proyecto_id integer NOT NULL
);


ALTER TABLE public."administrarRolesPermisos_rol" OWNER TO zar;

--
-- Name: administrarRolesPermisos_rol_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarRolesPermisos_rol_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarRolesPermisos_rol_id_seq" OWNER TO zar;

--
-- Name: administrarRolesPermisos_rol_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarRolesPermisos_rol_id_seq" OWNED BY "administrarRolesPermisos_rol".id;


--
-- Name: administrarTipoItem_atributo; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarTipoItem_atributo" (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    tipo character varying(3) NOT NULL,
    "tipoDeItem_id" integer NOT NULL,
    descripcion text NOT NULL
);


ALTER TABLE public."administrarTipoItem_atributo" OWNER TO zar;

--
-- Name: administrarTipoItem_atributo_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarTipoItem_atributo_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarTipoItem_atributo_id_seq" OWNER TO zar;

--
-- Name: administrarTipoItem_atributo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarTipoItem_atributo_id_seq" OWNED BY "administrarTipoItem_atributo".id;


--
-- Name: administrarTipoItem_tipoitem; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarTipoItem_tipoitem" (
    id integer NOT NULL,
    nombre character varying(100) NOT NULL,
    fase_id integer NOT NULL,
    descripcion text NOT NULL
);


ALTER TABLE public."administrarTipoItem_tipoitem" OWNER TO zar;

--
-- Name: administrarTipoItem_tipoitem_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE "administrarTipoItem_tipoitem_id_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public."administrarTipoItem_tipoitem_id_seq" OWNER TO zar;

--
-- Name: administrarTipoItem_tipoitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE "administrarTipoItem_tipoitem_id_seq" OWNED BY "administrarTipoItem_tipoitem".id;


--
-- Name: autenticacion_usuario; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE autenticacion_usuario (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    telefono character varying(20) NOT NULL
);


ALTER TABLE public.autenticacion_usuario OWNER TO zar;

--
-- Name: autenticacion_usuario_groups; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE autenticacion_usuario_groups (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.autenticacion_usuario_groups OWNER TO zar;

--
-- Name: autenticacion_usuario_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE autenticacion_usuario_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.autenticacion_usuario_groups_id_seq OWNER TO zar;

--
-- Name: autenticacion_usuario_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE autenticacion_usuario_groups_id_seq OWNED BY autenticacion_usuario_groups.id;


--
-- Name: autenticacion_usuario_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE autenticacion_usuario_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.autenticacion_usuario_id_seq OWNER TO zar;

--
-- Name: autenticacion_usuario_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE autenticacion_usuario_id_seq OWNED BY autenticacion_usuario.id;


--
-- Name: autenticacion_usuario_user_permissions; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE autenticacion_usuario_user_permissions (
    id integer NOT NULL,
    usuario_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.autenticacion_usuario_user_permissions OWNER TO zar;

--
-- Name: autenticacion_usuario_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE autenticacion_usuario_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.autenticacion_usuario_user_permissions_id_seq OWNER TO zar;

--
-- Name: autenticacion_usuario_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE autenticacion_usuario_user_permissions_id_seq OWNED BY autenticacion_usuario_user_permissions.id;


--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO zar;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO zar;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO zar;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO zar;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO zar;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO zar;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO zar;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO zar;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO zar;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO zar;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO zar;

--
-- Name: guardian_groupobjectpermission; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE guardian_groupobjectpermission (
    id integer NOT NULL,
    permission_id integer NOT NULL,
    content_type_id integer NOT NULL,
    object_pk character varying(255) NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.guardian_groupobjectpermission OWNER TO zar;

--
-- Name: guardian_groupobjectpermission_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE guardian_groupobjectpermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.guardian_groupobjectpermission_id_seq OWNER TO zar;

--
-- Name: guardian_groupobjectpermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE guardian_groupobjectpermission_id_seq OWNED BY guardian_groupobjectpermission.id;


--
-- Name: guardian_userobjectpermission; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE guardian_userobjectpermission (
    id integer NOT NULL,
    permission_id integer NOT NULL,
    content_type_id integer NOT NULL,
    object_pk character varying(255) NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE public.guardian_userobjectpermission OWNER TO zar;

--
-- Name: guardian_userobjectpermission_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE guardian_userobjectpermission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.guardian_userobjectpermission_id_seq OWNER TO zar;

--
-- Name: guardian_userobjectpermission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE guardian_userobjectpermission_id_seq OWNED BY guardian_userobjectpermission.id;


--
-- Name: reversion_revision; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE reversion_revision (
    id integer NOT NULL,
    manager_slug character varying(200) NOT NULL,
    date_created timestamp with time zone NOT NULL,
    user_id integer,
    comment text NOT NULL
);


ALTER TABLE public.reversion_revision OWNER TO zar;

--
-- Name: reversion_revision_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE reversion_revision_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reversion_revision_id_seq OWNER TO zar;

--
-- Name: reversion_revision_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE reversion_revision_id_seq OWNED BY reversion_revision.id;


--
-- Name: reversion_version; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE reversion_version (
    id integer NOT NULL,
    revision_id integer NOT NULL,
    object_id text NOT NULL,
    object_id_int integer,
    content_type_id integer NOT NULL,
    format character varying(255) NOT NULL,
    serialized_data text NOT NULL,
    object_repr text NOT NULL
);


ALTER TABLE public.reversion_version OWNER TO zar;

--
-- Name: reversion_version_id_seq; Type: SEQUENCE; Schema: public; Owner: zar
--

CREATE SEQUENCE reversion_version_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reversion_version_id_seq OWNER TO zar;

--
-- Name: reversion_version_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: zar
--

ALTER SEQUENCE reversion_version_id_seq OWNED BY reversion_version.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarFases_fase" ALTER COLUMN id SET DEFAULT nextval('"administrarFases_fase_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campofile" ALTER COLUMN id SET DEFAULT nextval('"administrarItems_campofile_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campoimagen" ALTER COLUMN id SET DEFAULT nextval('"administrarItems_campoimagen_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_camponumero" ALTER COLUMN id SET DEFAULT nextval('"administrarItems_camponumero_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campotextocorto" ALTER COLUMN id SET DEFAULT nextval('"administrarItems_campotextocorto_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campotextolargo" ALTER COLUMN id SET DEFAULT nextval('"administrarItems_campotextolargo_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_itembase" ALTER COLUMN id SET DEFAULT nextval('"administrarItems_itembase_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_itembase_solicitudes" ALTER COLUMN id SET DEFAULT nextval('"administrarItems_itembase_solicitudes_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_itemrelacion" ALTER COLUMN id SET DEFAULT nextval('"administrarItems_itemrelacion_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarLineaBase_lineabase" ALTER COLUMN id SET DEFAULT nextval('"administrarLineaBase_lineabase_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarLineaBase_solicitudcambios" ALTER COLUMN id SET DEFAULT nextval('"administrarLineaBase_solicitudcambios_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarLineaBase_votacion" ALTER COLUMN id SET DEFAULT nextval('"administrarLineaBase_votacion_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarProyectos_proyecto" ALTER COLUMN id SET DEFAULT nextval('"administrarProyectos_proyecto_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarProyectos_usuariosvinculadosproyectos" ALTER COLUMN id SET DEFAULT nextval('"administrarProyectos_usuariosvinculadosproyectos_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarRolesPermisos_permiso" ALTER COLUMN id SET DEFAULT nextval('"administrarRolesPermisos_permiso_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarRolesPermisos_rol" ALTER COLUMN id SET DEFAULT nextval('"administrarRolesPermisos_rol_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarTipoItem_atributo" ALTER COLUMN id SET DEFAULT nextval('"administrarTipoItem_atributo_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarTipoItem_tipoitem" ALTER COLUMN id SET DEFAULT nextval('"administrarTipoItem_tipoitem_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY autenticacion_usuario ALTER COLUMN id SET DEFAULT nextval('autenticacion_usuario_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY autenticacion_usuario_groups ALTER COLUMN id SET DEFAULT nextval('autenticacion_usuario_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY autenticacion_usuario_user_permissions ALTER COLUMN id SET DEFAULT nextval('autenticacion_usuario_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY guardian_groupobjectpermission ALTER COLUMN id SET DEFAULT nextval('guardian_groupobjectpermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY guardian_userobjectpermission ALTER COLUMN id SET DEFAULT nextval('guardian_userobjectpermission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY reversion_revision ALTER COLUMN id SET DEFAULT nextval('reversion_revision_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY reversion_version ALTER COLUMN id SET DEFAULT nextval('reversion_version_id_seq'::regclass);


--
-- Data for Name: administrarFases_fase; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarFases_fase" (id, nombre, descripcion, estado, proyecto_id, nro_orden) FROM stdin;
3	Fase01	Descripcion de la fase 01.	FIN	1	1
4	Fase02	Descripcion de la fase 02.	FIN	1	2
5	Fase03	Descripcion de la fase 03.	FIN	1	3
8	Fase2	Descripcion de la fase 2	PEN	2	3
7	Fase1	Descripcion de la fase 1	DES	2	2
6	Fase0	Descripcion de la fase 0	FIN	2	1
12	Fase2	Descripcion de la fase 2	PEN	4	3
11	Fase1	Descripcion de la fase 1	DES	4	2
9	Fase0	Descripcion de la fase 0	FIN	4	1
\.


--
-- Name: administrarFases_fase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarFases_fase_id_seq"', 12, true);


--
-- Data for Name: administrarItems_campofile; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_campofile" (id, item_id, atributo_id, archivo) FROM stdin;
\.


--
-- Name: administrarItems_campofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_campofile_id_seq"', 1, false);


--
-- Data for Name: administrarItems_campoimagen; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_campoimagen" (id, item_id, atributo_id, imagen) FROM stdin;
\.


--
-- Name: administrarItems_campoimagen_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_campoimagen_id_seq"', 1, false);


--
-- Data for Name: administrarItems_camponumero; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_camponumero" (id, item_id, atributo_id, valor) FROM stdin;
1	4	2	0
\.


--
-- Name: administrarItems_camponumero_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_camponumero_id_seq"', 1, true);


--
-- Data for Name: administrarItems_campotextocorto; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_campotextocorto" (id, item_id, atributo_id, valor) FROM stdin;
1	5	3	<default>
2	7	5	<default>
3	9	8	<default>
\.


--
-- Name: administrarItems_campotextocorto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_campotextocorto_id_seq"', 3, true);


--
-- Data for Name: administrarItems_campotextolargo; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_campotextolargo" (id, item_id, atributo_id, valor) FROM stdin;
1	1	1	Datos del atributo 00.
2	2	1	<default>
3	3	1	Texto largo de prueba.
4	6	4	<default>
5	8	7	<default>
\.


--
-- Name: administrarItems_campotextolargo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_campotextolargo_id_seq"', 5, true);


--
-- Data for Name: administrarItems_itembase; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_itembase" (id, usuario_id, usuario_modificacion_id, nombre, descripcion, estado, fecha_creacion, fecha_modificacion, tipoitem_id, complejidad, costo, tiempo, version, linea_base_id) FROM stdin;
3	2	3	Item02	Descripcion del item 02	ELB	2014-06-20 21:47:12.112387-04	2014-06-20 21:59:14.061753-04	1	1	1	1	2	2
2	3	3	Item01	Descripcion del item 01	ELB	2014-06-20 21:29:54.886468-04	2014-06-20 21:52:29.852199-04	1	3	3	3	2	1
1	3	3	Item00	Descripcion del item 00.	ELB	2014-06-20 21:27:03.972-04	2014-06-20 22:43:34.265164-04	1	2	2	2	4	1
4	3	3	Item03	Descripcion del item 03.	ELB	2014-06-21 00:21:10.27673-04	2014-06-21 00:21:34.698432-04	2	5	5	5	3	3
5	3	3	Item04	Descripcion del item 04	ELB	2014-06-21 00:22:56.236389-04	2014-06-21 00:23:07.400184-04	3	6	6	6	2	4
6	2	2	Item1	Descripcion del item 00	ELB	2014-06-21 00:39:23.72629-04	2014-06-21 00:42:30.085506-04	4	1	1	1	1	5
7	2	2	Item2	Descripcion del item 2	ACT	2014-06-21 00:43:27.293878-04	2014-06-21 00:43:27.293543-04	5	1	1	1	1	\N
8	3	3	Item05	Descripcion del item 04	ELB	2014-06-21 01:00:40.541934-04	2014-06-21 01:00:51.401714-04	7	1	1	1	1	6
9	3	3	Item06	Descripcion del item 8	VAL	2014-06-21 01:01:31.478056-04	2014-06-21 01:01:40.249852-04	8	8	8	8	2	\N
\.


--
-- Name: administrarItems_itembase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_itembase_id_seq"', 9, true);


--
-- Data for Name: administrarItems_itembase_solicitudes; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_itembase_solicitudes" (id, itembase_id, solicitudcambios_id) FROM stdin;
6	1	6
19	1	19
\.


--
-- Name: administrarItems_itembase_solicitudes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_itembase_solicitudes_id_seq"', 19, true);


--
-- Data for Name: administrarItems_itemrelacion; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_itemrelacion" (id, "itemPadre_id", "itemHijo_id", estado) FROM stdin;
1	1	2	ACT
2	3	4	ACT
3	4	5	ACT
4	8	9	ACT
\.


--
-- Name: administrarItems_itemrelacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_itemrelacion_id_seq"', 4, true);


--
-- Data for Name: administrarLineaBase_lineabase; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarLineaBase_lineabase" (id, fase_id, fecha_creacion, fecha_modificacion, observaciones) FROM stdin;
1	3	2014-06-20	2014-06-20	Linea base 00
2	3	2014-06-20	2014-06-20	Linea base 01
3	4	2014-06-21	2014-06-21	Linea Base 01 de la fase 02
4	5	2014-06-21	2014-06-21	Linea Base 01 de la fase 03
5	6	2014-06-21	2014-06-21	Linea Base 01 de la fase 0
6	9	2014-06-21	2014-06-21	Linea base
\.


--
-- Name: administrarLineaBase_lineabase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarLineaBase_lineabase_id_seq"', 6, true);


--
-- Data for Name: administrarLineaBase_solicitudcambios; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarLineaBase_solicitudcambios" (id, usuario_id, fase_id, motivo, fecha_creacion, estado, costo, tiempo) FROM stdin;
6	3	3	Solicitud de prueba 1	2014-06-20 22:37:05.047545-04	CAN	5	5
19	3	3	Solicitud de prueba	2014-06-21 00:08:30.28756-04	EJC	5	5
\.


--
-- Name: administrarLineaBase_solicitudcambios_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarLineaBase_solicitudcambios_id_seq"', 19, true);


--
-- Data for Name: administrarLineaBase_votacion; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarLineaBase_votacion" (id, usuario_id, solicitud_id, voto, justificacion) FROM stdin;
13	3	19	GOOD	ok
14	4	19	GOOD	ok
15	2	19	GOOD	ok
\.


--
-- Name: administrarLineaBase_votacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarLineaBase_votacion_id_seq"', 15, true);


--
-- Data for Name: administrarProyectos_proyecto; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarProyectos_proyecto" (id, nombre, lider_proyecto_id, descripcion, fecha_creacion, fecha_inicio, fecha_fin, estado, observaciones) FROM stdin;
3	Proyecto02	4	Descripcion del proyecto 02.	2014-06-20	\N	\N	PEN	No hay observaciones
1	Proyecto00	3	Descripcion del proyecto 00	2014-06-20	2014-06-20	2014-06-21	FIN	No hay observaciones
2	Proyecto01	2	Descripcion del proyecto 01.	2014-06-20	2014-06-21	2014-07-05	ACT	No hay observaciones
4	Proyecto03	3	Descripcion del proyecto 03.	2014-06-20	2014-06-21	2014-07-12	ANU	No hay observaciones
\.


--
-- Name: administrarProyectos_proyecto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarProyectos_proyecto_id_seq"', 4, true);


--
-- Data for Name: administrarProyectos_usuariosvinculadosproyectos; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarProyectos_usuariosvinculadosproyectos" (id, cod_proyecto_id, cod_usuario_id, habilitado) FROM stdin;
1	1	3	t
2	2	2	t
3	3	4	t
4	4	3	t
5	1	2	t
6	1	4	t
7	2	4	t
8	2	3	t
9	3	3	t
10	3	2	t
11	4	2	t
12	4	4	t
\.


--
-- Name: administrarProyectos_usuariosvinculadosproyectos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarProyectos_usuariosvinculadosproyectos_id_seq"', 12, true);


--
-- Data for Name: administrarRolesPermisos_permiso; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarRolesPermisos_permiso" (id, code, nombre, descripcion) FROM stdin;
\.


--
-- Name: administrarRolesPermisos_permiso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarRolesPermisos_permiso_id_seq"', 1, false);


--
-- Data for Name: administrarRolesPermisos_rol; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarRolesPermisos_rol" (id, grupo_id, proyecto_id) FROM stdin;
1	1	1
2	2	2
3	3	3
4	4	4
6	6	1
7	7	2
8	8	4
\.


--
-- Name: administrarRolesPermisos_rol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarRolesPermisos_rol_id_seq"', 8, true);


--
-- Data for Name: administrarTipoItem_atributo; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarTipoItem_atributo" (id, nombre, tipo, "tipoDeItem_id", descripcion) FROM stdin;
1	Atributo00	TXT	1	Descripcion del atributo 00.
2	Atributo00	NUM	2	Descripcion del atributo 00.
3	Atributo00	STR	3	Descripcion del atributo 00.
4	Atributo00	TXT	4	Descripcion del atributo 00.
5	Atributo00	STR	5	Descripcion del atributo 00.
6	Atributo00	NUM	6	Descripcion del atributo 00.
7	Atributo00	TXT	7	Descripcion del atributo 00.
8	Atributo00	STR	8	Descripcion del atributo 00.
9	Atributo00	NUM	9	Descripcion del atributo 00.
\.


--
-- Name: administrarTipoItem_atributo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarTipoItem_atributo_id_seq"', 9, true);


--
-- Data for Name: administrarTipoItem_tipoitem; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarTipoItem_tipoitem" (id, nombre, fase_id, descripcion) FROM stdin;
1	Tipo00	3	Descripcion del tipo de item 00.
2	Tipo01	4	Descripcion del tipo de item 01.
3	Tipo02	5	Descripcion del tipo de item 02.
4	Tipo00	6	Descripcion del tipo de item 00.
5	Tipo01	7	Descripcion del tipo de item 01.
6	Tipo02	8	Descripcion del tipo de item 02.
7	Tipo00	9	Descripcion del tipo de item 00.
9	Tipo02	12	Descripcion del tipo de item 02.
8	Tipo01	11	Descripcion del tipo de item 01.
\.


--
-- Name: administrarTipoItem_tipoitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarTipoItem_tipoitem_id_seq"', 9, true);


--
-- Data for Name: autenticacion_usuario; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY autenticacion_usuario (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, telefono) FROM stdin;
-1		2014-06-20 20:00:41.752504-04	f	AnonymousUser				f	t	2014-06-20 20:00:41.752577-04	
2	pbkdf2_sha256$12000$CcUYuwfAJhFw$ETLegJoT/9BqZPvxjE8DgzgiFvF0lYPn9Zviyga1454=	2014-06-21 00:32:28.643707-04	f	augusto	Augusto	Amarilla	agu.amarilla@gmail.com	f	t	2014-06-20 20:09:23.800495-04	456789
4	pbkdf2_sha256$12000$ewgiDWvyl4rA$RLLWfJQt7XI9Sq2s7vT760at9mR72YXoep1waHE7o4M=	2014-06-21 00:43:44.363885-04	f	saul	Saul	Zalimben	szalimben93@gmail.com	f	t	2014-06-20 20:17:02.298192-04	963258
1	pbkdf2_sha256$12000$DSCplnNVG8GH$rRsxFCGI0UF+K51hqmSuvS88mB3EMPKb26csaNRJVAs=	2014-06-21 01:02:29.540901-04	t	admin	Admin	Administrador	admitres03@gmail.com	t	t	2014-06-20 20:00:41.278974-04	123456
3	pbkdf2_sha256$12000$xTjg1Ttt3mkl$AJXKcFhQ1tEcUn6iH2SB02jzrcs8FhzJ6jTusumw+w0=	2014-06-21 01:03:09.803612-04	f	gerardo	Gerardo	Ramos	ragen93@gmail.com	f	t	2014-06-20 20:10:20.899015-04	741258
\.


--
-- Data for Name: autenticacion_usuario_groups; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY autenticacion_usuario_groups (id, usuario_id, group_id) FROM stdin;
5	4	3
24	3	1
25	2	1
26	4	1
27	4	6
28	2	6
29	3	6
30	2	2
31	4	2
32	3	2
33	4	7
34	3	7
35	2	7
36	3	4
37	2	4
38	4	4
42	2	8
43	4	8
44	3	8
\.


--
-- Name: autenticacion_usuario_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('autenticacion_usuario_groups_id_seq', 44, true);


--
-- Name: autenticacion_usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('autenticacion_usuario_id_seq', 4, true);


--
-- Data for Name: autenticacion_usuario_user_permissions; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY autenticacion_usuario_user_permissions (id, usuario_id, permission_id) FROM stdin;
\.


--
-- Name: autenticacion_usuario_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('autenticacion_usuario_user_permissions_id_seq', 1, false);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY auth_group (id, name) FROM stdin;
1	ComiteDeCambios-1
2	ComiteDeCambios-2
3	ComiteDeCambios-3
4	ComiteDeCambios-4
6	Super
7	Super1
8	Super2
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('auth_group_id_seq', 8, true);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Puede crear permiso	1	crear_permission
2	Puede modificar permiso	1	modificar_permission
3	Puede borrar permiso	1	borrar_permission
4	Puede crear grupo	2	crear_group
5	Puede modificar grupo	2	modificar_group
6	Puede borrar grupo	2	borrar_group
7	Puede crear tipo de contenido	3	crear_contenttype
8	Puede modificar tipo de contenido	3	modificar_contenttype
9	Puede borrar tipo de contenido	3	borrar_contenttype
10	Puede crear sesión	4	crear_session
11	Puede modificar sesión	4	modificar_session
12	Puede borrar sesión	4	borrar_session
13	Puede crear entrada de registro	5	crear_logentry
14	Puede modificar entrada de registro	5	modificar_logentry
15	Puede borrar entrada de registro	5	borrar_logentry
16	Puede crear revision	6	crear_revision
17	Puede modificar revision	6	modificar_revision
18	Puede borrar revision	6	borrar_revision
19	Puede crear version	7	crear_version
20	Puede modificar version	7	modificar_version
21	Puede borrar version	7	borrar_version
22	Puede crear usuario	8	crear_usuario
23	Puede modificar usuario	8	modificar_usuario
24	Puede borrar usuario	8	borrar_usuario
25	Puede crear proyecto	9	crear_proyecto
26	Puede modificar proyecto	9	modificar_proyecto
27	Puede borrar proyecto	9	borrar_proyecto
28	Puede consultar proyecto	9	consultar_Proyecto
29	Puede consultar usuarios vinculados	9	consultar_Usuarios_Vinculados
30	Puede crear usuarios vinculados proyectos	10	crear_usuariosvinculadosproyectos
31	Puede modificar usuarios vinculados proyectos	10	modificar_usuariosvinculadosproyectos
32	Puede borrar usuarios vinculados proyectos	10	borrar_usuariosvinculadosproyectos
33	Puede crear fase	11	crear_fase
34	Puede modificar fase	11	modificar_fase
35	Puede borrar fase	11	borrar_fase
36	Puede crear items	11	crear_Item
37	Puede modificar items	11	modificar_Item
38	Puede dar de baja items	11	dar_de_baja_Item
39	Puede restaurar items	11	restaurar_Item
40	Puede revertir items	11	revertir_Item
41	Puede consultar items	11	consultar_Item
42	Puede consultar fases	11	consultar_Fase
43	Puede consultar tipos de item	11	consultar_Tipo_Item
44	Puede consultar lineas base	11	consultar_Lineas_Base
45	Puede crear solicitudes de cambio	11	crear_Solicitud_Cambio
46	Puede crear lineas base	11	crear_Linea_Base
47	Puede crear permiso	12	crear_permiso
48	Puede modificar permiso	12	modificar_permiso
49	Puede borrar permiso	12	borrar_permiso
50	Puede crear rol	13	crear_rol
51	Puede modificar rol	13	modificar_rol
52	Puede borrar rol	13	borrar_rol
53	Puede crear TipoItem	14	crear_tipoitem
54	Puede modificar TipoItem	14	modificar_tipoitem
55	Puede borrar TipoItem	14	borrar_tipoitem
56	Puede crear Atributo	15	crear_atributo
57	Puede modificar Atributo	15	modificar_atributo
58	Puede borrar Atributo	15	borrar_atributo
59	Puede crear item base	16	crear_itembase
60	Puede modificar item base	16	modificar_itembase
61	Puede borrar item base	16	borrar_itembase
62	Modificar Item de LB	16	credencial
63	Puede crear item relacion	17	crear_itemrelacion
64	Puede modificar item relacion	17	modificar_itemrelacion
65	Puede borrar item relacion	17	borrar_itemrelacion
66	Puede crear campo numero	18	crear_camponumero
67	Puede modificar campo numero	18	modificar_camponumero
68	Puede borrar campo numero	18	borrar_camponumero
69	Puede crear campo texto corto	19	crear_campotextocorto
70	Puede modificar campo texto corto	19	modificar_campotextocorto
71	Puede borrar campo texto corto	19	borrar_campotextocorto
72	Puede crear campo texto largo	20	crear_campotextolargo
73	Puede modificar campo texto largo	20	modificar_campotextolargo
74	Puede borrar campo texto largo	20	borrar_campotextolargo
75	Puede crear campo file	21	crear_campofile
76	Puede modificar campo file	21	modificar_campofile
77	Puede borrar campo file	21	borrar_campofile
78	Puede crear campo imagen	22	crear_campoimagen
79	Puede modificar campo imagen	22	modificar_campoimagen
80	Puede borrar campo imagen	22	borrar_campoimagen
81	Puede crear linea base	23	crear_lineabase
82	Puede modificar linea base	23	modificar_lineabase
83	Puede borrar linea base	23	borrar_lineabase
84	Puede crear solicitud	24	crear_solicitudcambios
85	Puede modificar solicitud	24	modificar_solicitudcambios
86	Puede borrar solicitud	24	borrar_solicitudcambios
87	Puede crear votacion	25	crear_votacion
88	Puede modificar votacion	25	modificar_votacion
89	Puede borrar votacion	25	borrar_votacion
90	Puede crear user object permission	26	crear_userobjectpermission
91	Puede modificar user object permission	26	modificar_userobjectpermission
92	Puede borrar user object permission	26	borrar_userobjectpermission
93	Puede crear group object permission	27	crear_groupobjectpermission
94	Puede modificar group object permission	27	modificar_groupobjectpermission
95	Puede borrar group object permission	27	borrar_groupobjectpermission
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('auth_permission_id_seq', 95, true);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	content type	contenttypes	contenttype
4	session	sessions	session
5	log entry	admin	logentry
6	revision	reversion	revision
7	version	reversion	version
8	user	autenticacion	usuario
9	proyecto	administrarProyectos	proyecto
10	usuarios vinculados proyectos	administrarProyectos	usuariosvinculadosproyectos
11	fase	administrarFases	fase
12	permiso	administrarRolesPermisos	permiso
13	rol	administrarRolesPermisos	rol
14	TipoItem	administrarTipoItem	tipoitem
15	Atributo	administrarTipoItem	atributo
16	item base	administrarItems	itembase
17	item relacion	administrarItems	itemrelacion
18	campo numero	administrarItems	camponumero
19	campo texto corto	administrarItems	campotextocorto
20	campo texto largo	administrarItems	campotextolargo
21	campo file	administrarItems	campofile
22	campo imagen	administrarItems	campoimagen
23	linea base	administrarLineaBase	lineabase
24	solicitud	administrarLineaBase	solicitudcambios
25	votacion	administrarLineaBase	votacion
26	user object permission	guardian	userobjectpermission
27	group object permission	guardian	groupobjectpermission
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('django_content_type_id_seq', 27, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
tr2ojdheiwbeok5t28rfopof0edsqkcs	YmQ0YzczZGQ4MmE3ZjYxNGY0ODhhYzU5ZDlkYmZkY2Q2MGQwZmU2OTp7Il9hdXRoX3VzZXJfYmFja2VuZCI6ImRqYW5nby5jb250cmliLmF1dGguYmFja2VuZHMuTW9kZWxCYWNrZW5kIiwiX2F1dGhfdXNlcl9pZCI6MSwiX3Nlc3Npb25fZXhwaXJ5IjowfQ==	2014-07-04 20:04:14.655904-04
cyovf9s626p3kuk7yi52n612jnq2f5ku	ZmE0MTYwNzBiMTZiMWVmYzI3ZjI3N2JiYjAzYzRlNWNhMGFkZjg0NTp7InJldG9ybm8iOiIvaW5mb3Byb2plY3QvNCIsIl9zZXNzaW9uX2V4cGlyeSI6MCwiX2F1dGhfdXNlcl9pZCI6MywiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQifQ==	2014-07-05 01:03:13.67234-04
86ysaix3hl7og0i7ld8ev8tjehuykyts	MzYzNDcwMDZhNjMwM2YzNzkwYzI1YjlmNWE5MWY5NDEwNDFjY2I0YTp7InJldG9ybm8iOiIvZGVzYXJyb2xsby80IiwiX2F1dGhfdXNlcl9pZCI6MywiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfc2Vzc2lvbl9leHBpcnkiOjB9	2014-07-05 00:58:49.455302-04
\.


--
-- Data for Name: guardian_groupobjectpermission; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY guardian_groupobjectpermission (id, permission_id, content_type_id, object_pk, group_id) FROM stdin;
3	28	9	1	6
4	29	9	1	6
27	36	11	3	6
28	37	11	3	6
29	38	11	3	6
30	39	11	3	6
31	40	11	3	6
32	41	11	3	6
33	42	11	3	6
34	43	11	3	6
35	44	11	3	6
36	45	11	3	6
37	46	11	3	6
38	36	11	5	6
39	37	11	5	6
40	38	11	5	6
41	39	11	5	6
42	40	11	5	6
43	41	11	5	6
44	42	11	5	6
45	43	11	5	6
46	44	11	5	6
47	45	11	5	6
48	46	11	5	6
49	36	11	4	6
50	37	11	4	6
51	38	11	4	6
52	39	11	4	6
53	40	11	4	6
54	41	11	4	6
55	42	11	4	6
56	43	11	4	6
57	44	11	4	6
58	45	11	4	6
59	46	11	4	6
60	28	9	2	7
61	29	9	2	7
62	36	11	6	7
63	37	11	6	7
64	38	11	6	7
65	39	11	6	7
66	40	11	6	7
67	41	11	6	7
68	42	11	6	7
69	43	11	6	7
70	44	11	6	7
71	45	11	6	7
72	46	11	6	7
73	36	11	7	7
74	37	11	7	7
75	38	11	7	7
76	39	11	7	7
77	40	11	7	7
78	41	11	7	7
79	42	11	7	7
80	43	11	7	7
81	44	11	7	7
82	45	11	7	7
83	46	11	7	7
84	36	11	8	7
85	37	11	8	7
86	38	11	8	7
87	39	11	8	7
88	40	11	8	7
89	41	11	8	7
90	42	11	8	7
91	43	11	8	7
92	44	11	8	7
93	45	11	8	7
94	46	11	8	7
95	28	9	4	8
96	29	9	4	8
97	36	11	12	8
98	37	11	12	8
99	38	11	12	8
100	39	11	12	8
101	40	11	12	8
102	41	11	12	8
103	42	11	12	8
104	43	11	12	8
105	44	11	12	8
106	45	11	12	8
107	46	11	12	8
108	36	11	9	8
109	37	11	9	8
110	38	11	9	8
111	39	11	9	8
112	40	11	9	8
113	41	11	9	8
114	42	11	9	8
115	43	11	9	8
116	44	11	9	8
117	45	11	9	8
118	46	11	9	8
119	36	11	11	8
120	37	11	11	8
121	38	11	11	8
122	39	11	11	8
123	40	11	11	8
124	41	11	11	8
125	42	11	11	8
126	43	11	11	8
127	44	11	11	8
128	45	11	11	8
129	46	11	11	8
\.


--
-- Name: guardian_groupobjectpermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('guardian_groupobjectpermission_id_seq', 129, true);


--
-- Data for Name: guardian_userobjectpermission; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY guardian_userobjectpermission (id, permission_id, content_type_id, object_pk, user_id) FROM stdin;
\.


--
-- Name: guardian_userobjectpermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('guardian_userobjectpermission_id_seq', 5, true);


--
-- Data for Name: reversion_revision; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY reversion_revision (id, manager_slug, date_created, user_id, comment) FROM stdin;
1	default	2014-06-20 21:27:04.040453-04	\N	
2	default	2014-06-20 21:27:42.245419-04	\N	
3	default	2014-06-20 21:27:51.132686-04	\N	
4	default	2014-06-20 21:29:54.948559-04	\N	
5	default	2014-06-20 21:30:23.720673-04	\N	
6	default	2014-06-20 21:47:12.181072-04	\N	
7	default	2014-06-20 21:52:57.570199-04	\N	
8	default	2014-06-20 22:43:34.337723-04	\N	
9	default	2014-06-21 00:21:10.372445-04	\N	
10	default	2014-06-21 00:21:17.855284-04	\N	
11	default	2014-06-21 00:21:29.74783-04	\N	
12	default	2014-06-21 00:22:56.298392-04	\N	
13	default	2014-06-21 00:23:04.001864-04	\N	
14	default	2014-06-21 00:39:23.805221-04	\N	
15	default	2014-06-21 00:43:27.390385-04	\N	
16	default	2014-06-21 01:00:40.689492-04	\N	
17	default	2014-06-21 01:01:31.572064-04	\N	
18	default	2014-06-21 01:01:36.950252-04	\N	
\.


--
-- Name: reversion_revision_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('reversion_revision_id_seq', 18, true);


--
-- Data for Name: reversion_version; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY reversion_version (id, revision_id, object_id, object_id_int, content_type_id, format, serialized_data, object_repr) FROM stdin;
1	1	1	1	16	json	[{"pk": 1, "model": "administrarItems.itembase", "fields": {"tiempo": 1, "usuario": 3, "fecha_creacion": "2014-06-21T01:27:03.972Z", "linea_base": null, "solicitudes": [], "tipoitem": 1, "version": 1, "complejidad": 1, "descripcion": "Descripcion del item 00.", "nombre": "Item00", "costo": 1, "estado": "ACT", "fecha_modificacion": "2014-06-21T01:27:03.972Z", "usuario_modificacion": 3}}]	Item00
2	1	1	1	20	json	[{"pk": 1, "model": "administrarItems.campotextolargo", "fields": {"item": 1, "atributo": 1, "valor": "<default>"}}]	CampoTextoLargo object
3	2	1	1	16	json	[{"pk": 1, "model": "administrarItems.itembase", "fields": {"tiempo": -2, "usuario": 3, "fecha_creacion": "2014-06-21T01:27:03.972Z", "linea_base": null, "solicitudes": [], "tipoitem": 1, "version": 2, "complejidad": 2, "descripcion": "Descripcion del item 00.", "nombre": "Item00", "costo": 2, "estado": "ACT", "fecha_modificacion": "2014-06-21T01:27:42.230Z", "usuario_modificacion": 3}}]	Item00
4	2	1	1	20	json	[{"pk": 1, "model": "administrarItems.campotextolargo", "fields": {"item": 1, "atributo": 1, "valor": "Datos del atributo 00."}}]	CampoTextoLargo object
5	3	1	1	16	json	[{"pk": 1, "model": "administrarItems.itembase", "fields": {"tiempo": 2, "usuario": 3, "fecha_creacion": "2014-06-21T01:27:03.972Z", "linea_base": null, "solicitudes": [], "tipoitem": 1, "version": 3, "complejidad": 2, "descripcion": "Descripcion del item 00.", "nombre": "Item00", "costo": 2, "estado": "ACT", "fecha_modificacion": "2014-06-21T01:27:51.115Z", "usuario_modificacion": 3}}]	Item00
6	4	2	2	16	json	[{"pk": 2, "model": "administrarItems.itembase", "fields": {"tiempo": 3, "usuario": 3, "fecha_creacion": "2014-06-21T01:29:54.886Z", "linea_base": null, "solicitudes": [], "tipoitem": 1, "version": 1, "complejidad": 3, "descripcion": "Descripcion del item 01", "nombre": "Item01", "costo": 3, "estado": "ACT", "fecha_modificacion": "2014-06-21T01:29:54.886Z", "usuario_modificacion": 3}}]	Item01
7	4	2	2	20	json	[{"pk": 2, "model": "administrarItems.campotextolargo", "fields": {"item": 2, "atributo": 1, "valor": "<default>"}}]	CampoTextoLargo object
8	5	1	1	17	json	[{"pk": 1, "model": "administrarItems.itemrelacion", "fields": {"itemPadre": 1, "estado": "ACT", "itemHijo": 2}}]	ItemRelacion object
9	5	2	2	16	json	[{"pk": 2, "model": "administrarItems.itembase", "fields": {"tiempo": 3, "usuario": 3, "fecha_creacion": "2014-06-21T01:29:54.886Z", "linea_base": null, "solicitudes": [], "tipoitem": 1, "version": 2, "complejidad": 3, "descripcion": "Descripcion del item 01", "nombre": "Item01", "costo": 3, "estado": "ACT", "fecha_modificacion": "2014-06-21T01:30:23.697Z", "usuario_modificacion": 3}}]	Item01
10	6	3	3	16	json	[{"pk": 3, "model": "administrarItems.itembase", "fields": {"tiempo": 1, "usuario": 2, "fecha_creacion": "2014-06-21T01:47:12.112Z", "linea_base": null, "solicitudes": [], "tipoitem": 1, "version": 1, "complejidad": 1, "descripcion": "Descripcion del item 02.", "nombre": "Item02", "costo": 1, "estado": "ACT", "fecha_modificacion": "2014-06-21T01:47:12.112Z", "usuario_modificacion": 2}}]	Item02
11	6	3	3	20	json	[{"pk": 3, "model": "administrarItems.campotextolargo", "fields": {"item": 3, "atributo": 1, "valor": "<default>"}}]	CampoTextoLargo object
12	7	3	3	16	json	[{"pk": 3, "model": "administrarItems.itembase", "fields": {"tiempo": 1, "usuario": 2, "fecha_creacion": "2014-06-21T01:47:12.112Z", "linea_base": null, "solicitudes": [], "tipoitem": 1, "version": 2, "complejidad": 1, "descripcion": "Descripcion del item 02", "nombre": "Item02", "costo": 1, "estado": "ACT", "fecha_modificacion": "2014-06-21T01:52:57.558Z", "usuario_modificacion": 3}}]	Item02
13	7	3	3	20	json	[{"pk": 3, "model": "administrarItems.campotextolargo", "fields": {"item": 3, "atributo": 1, "valor": "Texto largo de prueba."}}]	CampoTextoLargo object
14	8	1	1	16	json	[{"pk": 1, "model": "administrarItems.itembase", "fields": {"tiempo": 2, "usuario": 3, "fecha_creacion": "2014-06-21T01:27:03.972Z", "linea_base": 1, "solicitudes": [6, 7], "tipoitem": 1, "version": 4, "complejidad": 2, "descripcion": "Descripcion del item 00.", "nombre": "Item00", "costo": 2, "estado": "REV", "fecha_modificacion": "2014-06-21T02:43:34.265Z", "usuario_modificacion": 3}}]	Item00
15	9	1	1	18	json	[{"pk": 1, "model": "administrarItems.camponumero", "fields": {"item": 4, "atributo": 2, "valor": 0}}]	CampoNumero object
16	9	4	4	16	json	[{"pk": 4, "model": "administrarItems.itembase", "fields": {"tiempo": 5, "usuario": 3, "fecha_creacion": "2014-06-21T04:21:10.276Z", "linea_base": null, "solicitudes": [], "tipoitem": 2, "version": 1, "complejidad": 5, "descripcion": "Descripcion del item 00.", "nombre": "Item03", "costo": 5, "estado": "ACT", "fecha_modificacion": "2014-06-21T04:21:10.276Z", "usuario_modificacion": 3}}]	Item03
17	10	4	4	16	json	[{"pk": 4, "model": "administrarItems.itembase", "fields": {"tiempo": 5, "usuario": 3, "fecha_creacion": "2014-06-21T04:21:10.276Z", "linea_base": null, "solicitudes": [], "tipoitem": 2, "version": 2, "complejidad": 5, "descripcion": "Descripcion del item 03.", "nombre": "Item03", "costo": 5, "estado": "ACT", "fecha_modificacion": "2014-06-21T04:21:17.837Z", "usuario_modificacion": 3}}]	Item03
18	11	2	2	17	json	[{"pk": 2, "model": "administrarItems.itemrelacion", "fields": {"itemPadre": 3, "estado": "ACT", "itemHijo": 4}}]	ItemRelacion object
19	11	4	4	16	json	[{"pk": 4, "model": "administrarItems.itembase", "fields": {"tiempo": 5, "usuario": 3, "fecha_creacion": "2014-06-21T04:21:10.276Z", "linea_base": null, "solicitudes": [], "tipoitem": 2, "version": 3, "complejidad": 5, "descripcion": "Descripcion del item 03.", "nombre": "Item03", "costo": 5, "estado": "ACT", "fecha_modificacion": "2014-06-21T04:21:29.732Z", "usuario_modificacion": 3}}]	Item03
20	12	1	1	19	json	[{"pk": 1, "model": "administrarItems.campotextocorto", "fields": {"item": 5, "atributo": 3, "valor": "<default>"}}]	CampoTextoCorto object
21	12	5	5	16	json	[{"pk": 5, "model": "administrarItems.itembase", "fields": {"tiempo": 6, "usuario": 3, "fecha_creacion": "2014-06-21T04:22:56.236Z", "linea_base": null, "solicitudes": [], "tipoitem": 3, "version": 1, "complejidad": 6, "descripcion": "Descripcion del item 04", "nombre": "Item04", "costo": 6, "estado": "ACT", "fecha_modificacion": "2014-06-21T04:22:56.236Z", "usuario_modificacion": 3}}]	Item04
22	13	3	3	17	json	[{"pk": 3, "model": "administrarItems.itemrelacion", "fields": {"itemPadre": 4, "estado": "ACT", "itemHijo": 5}}]	ItemRelacion object
23	13	5	5	16	json	[{"pk": 5, "model": "administrarItems.itembase", "fields": {"tiempo": 6, "usuario": 3, "fecha_creacion": "2014-06-21T04:22:56.236Z", "linea_base": null, "solicitudes": [], "tipoitem": 3, "version": 2, "complejidad": 6, "descripcion": "Descripcion del item 04", "nombre": "Item04", "costo": 6, "estado": "ACT", "fecha_modificacion": "2014-06-21T04:23:03.990Z", "usuario_modificacion": 3}}]	Item04
24	14	4	4	20	json	[{"pk": 4, "model": "administrarItems.campotextolargo", "fields": {"item": 6, "atributo": 4, "valor": "<default>"}}]	CampoTextoLargo object
25	14	6	6	16	json	[{"pk": 6, "model": "administrarItems.itembase", "fields": {"tiempo": 1, "usuario": 2, "fecha_creacion": "2014-06-21T04:39:23.726Z", "linea_base": null, "solicitudes": [], "tipoitem": 4, "version": 1, "complejidad": 1, "descripcion": "Descripcion del item 00", "nombre": "Item1", "costo": 1, "estado": "ACT", "fecha_modificacion": "2014-06-21T04:39:23.725Z", "usuario_modificacion": 2}}]	Item1
26	15	2	2	19	json	[{"pk": 2, "model": "administrarItems.campotextocorto", "fields": {"item": 7, "atributo": 5, "valor": "<default>"}}]	CampoTextoCorto object
27	15	7	7	16	json	[{"pk": 7, "model": "administrarItems.itembase", "fields": {"tiempo": 1, "usuario": 2, "fecha_creacion": "2014-06-21T04:43:27.293Z", "linea_base": null, "solicitudes": [], "tipoitem": 5, "version": 1, "complejidad": 1, "descripcion": "Descripcion del item 2", "nombre": "Item2", "costo": 1, "estado": "ACT", "fecha_modificacion": "2014-06-21T04:43:27.293Z", "usuario_modificacion": 2}}]	Item2
28	16	8	8	16	json	[{"pk": 8, "model": "administrarItems.itembase", "fields": {"tiempo": 1, "usuario": 3, "fecha_creacion": "2014-06-21T05:00:40.541Z", "linea_base": null, "solicitudes": [], "tipoitem": 7, "version": 1, "complejidad": 1, "descripcion": "Descripcion del item 04", "nombre": "Item05", "costo": 1, "estado": "ACT", "fecha_modificacion": "2014-06-21T05:00:40.541Z", "usuario_modificacion": 3}}]	Item05
29	16	5	5	20	json	[{"pk": 5, "model": "administrarItems.campotextolargo", "fields": {"item": 8, "atributo": 7, "valor": "<default>"}}]	CampoTextoLargo object
30	17	9	9	16	json	[{"pk": 9, "model": "administrarItems.itembase", "fields": {"tiempo": 8, "usuario": 3, "fecha_creacion": "2014-06-21T05:01:31.478Z", "linea_base": null, "solicitudes": [], "tipoitem": 8, "version": 1, "complejidad": 8, "descripcion": "Descripcion del item 8", "nombre": "Item06", "costo": 8, "estado": "ACT", "fecha_modificacion": "2014-06-21T05:01:31.477Z", "usuario_modificacion": 3}}]	Item06
31	17	3	3	19	json	[{"pk": 3, "model": "administrarItems.campotextocorto", "fields": {"item": 9, "atributo": 8, "valor": "<default>"}}]	CampoTextoCorto object
32	18	9	9	16	json	[{"pk": 9, "model": "administrarItems.itembase", "fields": {"tiempo": 8, "usuario": 3, "fecha_creacion": "2014-06-21T05:01:31.478Z", "linea_base": null, "solicitudes": [], "tipoitem": 8, "version": 2, "complejidad": 8, "descripcion": "Descripcion del item 8", "nombre": "Item06", "costo": 8, "estado": "ACT", "fecha_modificacion": "2014-06-21T05:01:36.937Z", "usuario_modificacion": 3}}]	Item06
33	18	4	4	17	json	[{"pk": 4, "model": "administrarItems.itemrelacion", "fields": {"itemPadre": 8, "estado": "ACT", "itemHijo": 9}}]	ItemRelacion object
\.


--
-- Name: reversion_version_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('reversion_version_id_seq', 33, true);


--
-- Name: administrarFases_fase_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarFases_fase"
    ADD CONSTRAINT "administrarFases_fase_pkey" PRIMARY KEY (id);


--
-- Name: administrarFases_fase_proyecto_id_nombre_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarFases_fase"
    ADD CONSTRAINT "administrarFases_fase_proyecto_id_nombre_key" UNIQUE (proyecto_id, nombre);


--
-- Name: administrarItems_campofile_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarItems_campofile"
    ADD CONSTRAINT "administrarItems_campofile_pkey" PRIMARY KEY (id);


--
-- Name: administrarItems_campoimagen_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarItems_campoimagen"
    ADD CONSTRAINT "administrarItems_campoimagen_pkey" PRIMARY KEY (id);


--
-- Name: administrarItems_camponumero_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarItems_camponumero"
    ADD CONSTRAINT "administrarItems_camponumero_pkey" PRIMARY KEY (id);


--
-- Name: administrarItems_campotextocorto_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarItems_campotextocorto"
    ADD CONSTRAINT "administrarItems_campotextocorto_pkey" PRIMARY KEY (id);


--
-- Name: administrarItems_campotextolargo_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarItems_campotextolargo"
    ADD CONSTRAINT "administrarItems_campotextolargo_pkey" PRIMARY KEY (id);


--
-- Name: administrarItems_itembase_nombre_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarItems_itembase"
    ADD CONSTRAINT "administrarItems_itembase_nombre_key" UNIQUE (nombre);


--
-- Name: administrarItems_itembase_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarItems_itembase"
    ADD CONSTRAINT "administrarItems_itembase_pkey" PRIMARY KEY (id);


--
-- Name: administrarItems_itembase_sol_itembase_id_solicitudcambios__key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarItems_itembase_solicitudes"
    ADD CONSTRAINT "administrarItems_itembase_sol_itembase_id_solicitudcambios__key" UNIQUE (itembase_id, solicitudcambios_id);


--
-- Name: administrarItems_itembase_solicitudes_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarItems_itembase_solicitudes"
    ADD CONSTRAINT "administrarItems_itembase_solicitudes_pkey" PRIMARY KEY (id);


--
-- Name: administrarItems_itemrelacion_itemHijo_id_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarItems_itemrelacion"
    ADD CONSTRAINT "administrarItems_itemrelacion_itemHijo_id_key" UNIQUE ("itemHijo_id");


--
-- Name: administrarItems_itemrelacion_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarItems_itemrelacion"
    ADD CONSTRAINT "administrarItems_itemrelacion_pkey" PRIMARY KEY (id);


--
-- Name: administrarLineaBase_lineabase_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarLineaBase_lineabase"
    ADD CONSTRAINT "administrarLineaBase_lineabase_pkey" PRIMARY KEY (id);


--
-- Name: administrarLineaBase_solicitudcambios_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarLineaBase_solicitudcambios"
    ADD CONSTRAINT "administrarLineaBase_solicitudcambios_pkey" PRIMARY KEY (id);


--
-- Name: administrarLineaBase_votacion_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarLineaBase_votacion"
    ADD CONSTRAINT "administrarLineaBase_votacion_pkey" PRIMARY KEY (id);


--
-- Name: administrarProyectos_proyecto_nombre_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarProyectos_proyecto"
    ADD CONSTRAINT "administrarProyectos_proyecto_nombre_key" UNIQUE (nombre);


--
-- Name: administrarProyectos_proyecto_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarProyectos_proyecto"
    ADD CONSTRAINT "administrarProyectos_proyecto_pkey" PRIMARY KEY (id);


--
-- Name: administrarProyectos_usuarios_cod_proyecto_id_cod_usuario_i_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarProyectos_usuariosvinculadosproyectos"
    ADD CONSTRAINT "administrarProyectos_usuarios_cod_proyecto_id_cod_usuario_i_key" UNIQUE (cod_proyecto_id, cod_usuario_id);


--
-- Name: administrarProyectos_usuariosvinculadosproyectos_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarProyectos_usuariosvinculadosproyectos"
    ADD CONSTRAINT "administrarProyectos_usuariosvinculadosproyectos_pkey" PRIMARY KEY (id);


--
-- Name: administrarRolesPermisos_permiso_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarRolesPermisos_permiso"
    ADD CONSTRAINT "administrarRolesPermisos_permiso_pkey" PRIMARY KEY (id);


--
-- Name: administrarRolesPermisos_rol_grupo_id_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarRolesPermisos_rol"
    ADD CONSTRAINT "administrarRolesPermisos_rol_grupo_id_key" UNIQUE (grupo_id);


--
-- Name: administrarRolesPermisos_rol_grupo_id_proyecto_id_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarRolesPermisos_rol"
    ADD CONSTRAINT "administrarRolesPermisos_rol_grupo_id_proyecto_id_key" UNIQUE (grupo_id, proyecto_id);


--
-- Name: administrarRolesPermisos_rol_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarRolesPermisos_rol"
    ADD CONSTRAINT "administrarRolesPermisos_rol_pkey" PRIMARY KEY (id);


--
-- Name: administrarTipoItem_atributo_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarTipoItem_atributo"
    ADD CONSTRAINT "administrarTipoItem_atributo_pkey" PRIMARY KEY (id);


--
-- Name: administrarTipoItem_atributo_tipoDeItem_id_nombre_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarTipoItem_atributo"
    ADD CONSTRAINT "administrarTipoItem_atributo_tipoDeItem_id_nombre_key" UNIQUE ("tipoDeItem_id", nombre);


--
-- Name: administrarTipoItem_tipoitem_fase_id_nombre_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarTipoItem_tipoitem"
    ADD CONSTRAINT "administrarTipoItem_tipoitem_fase_id_nombre_key" UNIQUE (fase_id, nombre);


--
-- Name: administrarTipoItem_tipoitem_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY "administrarTipoItem_tipoitem"
    ADD CONSTRAINT "administrarTipoItem_tipoitem_pkey" PRIMARY KEY (id);


--
-- Name: autenticacion_usuario_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY autenticacion_usuario_groups
    ADD CONSTRAINT autenticacion_usuario_groups_pkey PRIMARY KEY (id);


--
-- Name: autenticacion_usuario_groups_usuario_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY autenticacion_usuario_groups
    ADD CONSTRAINT autenticacion_usuario_groups_usuario_id_group_id_key UNIQUE (usuario_id, group_id);


--
-- Name: autenticacion_usuario_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY autenticacion_usuario
    ADD CONSTRAINT autenticacion_usuario_pkey PRIMARY KEY (id);


--
-- Name: autenticacion_usuario_user_permiss_usuario_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY autenticacion_usuario_user_permissions
    ADD CONSTRAINT autenticacion_usuario_user_permiss_usuario_id_permission_id_key UNIQUE (usuario_id, permission_id);


--
-- Name: autenticacion_usuario_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY autenticacion_usuario_user_permissions
    ADD CONSTRAINT autenticacion_usuario_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: autenticacion_usuario_username_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY autenticacion_usuario
    ADD CONSTRAINT autenticacion_usuario_username_key UNIQUE (username);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_model_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: guardian_groupobjectpermissio_group_id_permission_id_object_key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY guardian_groupobjectpermission
    ADD CONSTRAINT guardian_groupobjectpermissio_group_id_permission_id_object_key UNIQUE (group_id, permission_id, object_pk);


--
-- Name: guardian_groupobjectpermission_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY guardian_groupobjectpermission
    ADD CONSTRAINT guardian_groupobjectpermission_pkey PRIMARY KEY (id);


--
-- Name: guardian_userobjectpermission_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY guardian_userobjectpermission
    ADD CONSTRAINT guardian_userobjectpermission_pkey PRIMARY KEY (id);


--
-- Name: guardian_userobjectpermission_user_id_permission_id_object__key; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY guardian_userobjectpermission
    ADD CONSTRAINT guardian_userobjectpermission_user_id_permission_id_object__key UNIQUE (user_id, permission_id, object_pk);


--
-- Name: reversion_revision_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY reversion_revision
    ADD CONSTRAINT reversion_revision_pkey PRIMARY KEY (id);


--
-- Name: reversion_version_pkey; Type: CONSTRAINT; Schema: public; Owner: zar; Tablespace: 
--

ALTER TABLE ONLY reversion_version
    ADD CONSTRAINT reversion_version_pkey PRIMARY KEY (id);


--
-- Name: administrarFases_fase_proyecto_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarFases_fase_proyecto_id" ON "administrarFases_fase" USING btree (proyecto_id);


--
-- Name: administrarItems_campofile_atributo_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_campofile_atributo_id" ON "administrarItems_campofile" USING btree (atributo_id);


--
-- Name: administrarItems_campofile_item_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_campofile_item_id" ON "administrarItems_campofile" USING btree (item_id);


--
-- Name: administrarItems_campoimagen_atributo_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_campoimagen_atributo_id" ON "administrarItems_campoimagen" USING btree (atributo_id);


--
-- Name: administrarItems_campoimagen_item_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_campoimagen_item_id" ON "administrarItems_campoimagen" USING btree (item_id);


--
-- Name: administrarItems_camponumero_atributo_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_camponumero_atributo_id" ON "administrarItems_camponumero" USING btree (atributo_id);


--
-- Name: administrarItems_camponumero_item_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_camponumero_item_id" ON "administrarItems_camponumero" USING btree (item_id);


--
-- Name: administrarItems_campotextocorto_atributo_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_campotextocorto_atributo_id" ON "administrarItems_campotextocorto" USING btree (atributo_id);


--
-- Name: administrarItems_campotextocorto_item_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_campotextocorto_item_id" ON "administrarItems_campotextocorto" USING btree (item_id);


--
-- Name: administrarItems_campotextolargo_atributo_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_campotextolargo_atributo_id" ON "administrarItems_campotextolargo" USING btree (atributo_id);


--
-- Name: administrarItems_campotextolargo_item_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_campotextolargo_item_id" ON "administrarItems_campotextolargo" USING btree (item_id);


--
-- Name: administrarItems_itembase_linea_base_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_itembase_linea_base_id" ON "administrarItems_itembase" USING btree (linea_base_id);


--
-- Name: administrarItems_itembase_nombre_like; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_itembase_nombre_like" ON "administrarItems_itembase" USING btree (nombre varchar_pattern_ops);


--
-- Name: administrarItems_itembase_solicitudes_itembase_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_itembase_solicitudes_itembase_id" ON "administrarItems_itembase_solicitudes" USING btree (itembase_id);


--
-- Name: administrarItems_itembase_solicitudes_solicitudcambios_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_itembase_solicitudes_solicitudcambios_id" ON "administrarItems_itembase_solicitudes" USING btree (solicitudcambios_id);


--
-- Name: administrarItems_itembase_tipoitem_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_itembase_tipoitem_id" ON "administrarItems_itembase" USING btree (tipoitem_id);


--
-- Name: administrarItems_itembase_usuario_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_itembase_usuario_id" ON "administrarItems_itembase" USING btree (usuario_id);


--
-- Name: administrarItems_itembase_usuario_modificacion_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_itembase_usuario_modificacion_id" ON "administrarItems_itembase" USING btree (usuario_modificacion_id);


--
-- Name: administrarItems_itemrelacion_itemPadre_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarItems_itemrelacion_itemPadre_id" ON "administrarItems_itemrelacion" USING btree ("itemPadre_id");


--
-- Name: administrarLineaBase_lineabase_fase_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarLineaBase_lineabase_fase_id" ON "administrarLineaBase_lineabase" USING btree (fase_id);


--
-- Name: administrarLineaBase_solicitudcambios_fase_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarLineaBase_solicitudcambios_fase_id" ON "administrarLineaBase_solicitudcambios" USING btree (fase_id);


--
-- Name: administrarLineaBase_solicitudcambios_usuario_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarLineaBase_solicitudcambios_usuario_id" ON "administrarLineaBase_solicitudcambios" USING btree (usuario_id);


--
-- Name: administrarLineaBase_votacion_solicitud_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarLineaBase_votacion_solicitud_id" ON "administrarLineaBase_votacion" USING btree (solicitud_id);


--
-- Name: administrarLineaBase_votacion_usuario_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarLineaBase_votacion_usuario_id" ON "administrarLineaBase_votacion" USING btree (usuario_id);


--
-- Name: administrarProyectos_proyecto_lider_proyecto_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarProyectos_proyecto_lider_proyecto_id" ON "administrarProyectos_proyecto" USING btree (lider_proyecto_id);


--
-- Name: administrarProyectos_proyecto_nombre_like; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarProyectos_proyecto_nombre_like" ON "administrarProyectos_proyecto" USING btree (nombre varchar_pattern_ops);


--
-- Name: administrarProyectos_usuariosvinculadosproyectos_cod_proyecfac4; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarProyectos_usuariosvinculadosproyectos_cod_proyecfac4" ON "administrarProyectos_usuariosvinculadosproyectos" USING btree (cod_proyecto_id);


--
-- Name: administrarProyectos_usuariosvinculadosproyectos_cod_usuario_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarProyectos_usuariosvinculadosproyectos_cod_usuario_id" ON "administrarProyectos_usuariosvinculadosproyectos" USING btree (cod_usuario_id);


--
-- Name: administrarRolesPermisos_rol_proyecto_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarRolesPermisos_rol_proyecto_id" ON "administrarRolesPermisos_rol" USING btree (proyecto_id);


--
-- Name: administrarTipoItem_atributo_tipoDeItem_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarTipoItem_atributo_tipoDeItem_id" ON "administrarTipoItem_atributo" USING btree ("tipoDeItem_id");


--
-- Name: administrarTipoItem_tipoitem_fase_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX "administrarTipoItem_tipoitem_fase_id" ON "administrarTipoItem_tipoitem" USING btree (fase_id);


--
-- Name: autenticacion_usuario_groups_group_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX autenticacion_usuario_groups_group_id ON autenticacion_usuario_groups USING btree (group_id);


--
-- Name: autenticacion_usuario_groups_usuario_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX autenticacion_usuario_groups_usuario_id ON autenticacion_usuario_groups USING btree (usuario_id);


--
-- Name: autenticacion_usuario_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX autenticacion_usuario_user_permissions_permission_id ON autenticacion_usuario_user_permissions USING btree (permission_id);


--
-- Name: autenticacion_usuario_user_permissions_usuario_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX autenticacion_usuario_user_permissions_usuario_id ON autenticacion_usuario_user_permissions USING btree (usuario_id);


--
-- Name: autenticacion_usuario_username_like; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX autenticacion_usuario_username_like ON autenticacion_usuario USING btree (username varchar_pattern_ops);


--
-- Name: auth_group_name_like; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX auth_group_name_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX django_session_expire_date ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_like; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX django_session_session_key_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: guardian_groupobjectpermission_content_type_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX guardian_groupobjectpermission_content_type_id ON guardian_groupobjectpermission USING btree (content_type_id);


--
-- Name: guardian_groupobjectpermission_group_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX guardian_groupobjectpermission_group_id ON guardian_groupobjectpermission USING btree (group_id);


--
-- Name: guardian_groupobjectpermission_permission_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX guardian_groupobjectpermission_permission_id ON guardian_groupobjectpermission USING btree (permission_id);


--
-- Name: guardian_userobjectpermission_content_type_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX guardian_userobjectpermission_content_type_id ON guardian_userobjectpermission USING btree (content_type_id);


--
-- Name: guardian_userobjectpermission_permission_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX guardian_userobjectpermission_permission_id ON guardian_userobjectpermission USING btree (permission_id);


--
-- Name: guardian_userobjectpermission_user_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX guardian_userobjectpermission_user_id ON guardian_userobjectpermission USING btree (user_id);


--
-- Name: reversion_revision_manager_slug; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX reversion_revision_manager_slug ON reversion_revision USING btree (manager_slug);


--
-- Name: reversion_revision_manager_slug_like; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX reversion_revision_manager_slug_like ON reversion_revision USING btree (manager_slug varchar_pattern_ops);


--
-- Name: reversion_revision_user_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX reversion_revision_user_id ON reversion_revision USING btree (user_id);


--
-- Name: reversion_version_content_type_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX reversion_version_content_type_id ON reversion_version USING btree (content_type_id);


--
-- Name: reversion_version_object_id_int; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX reversion_version_object_id_int ON reversion_version USING btree (object_id_int);


--
-- Name: reversion_version_revision_id; Type: INDEX; Schema: public; Owner: zar; Tablespace: 
--

CREATE INDEX reversion_version_revision_id ON reversion_version USING btree (revision_id);


--
-- Name: administrarFases_fase_proyecto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarFases_fase"
    ADD CONSTRAINT "administrarFases_fase_proyecto_id_fkey" FOREIGN KEY (proyecto_id) REFERENCES "administrarProyectos_proyecto"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_campofile_atributo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campofile"
    ADD CONSTRAINT "administrarItems_campofile_atributo_id_fkey" FOREIGN KEY (atributo_id) REFERENCES "administrarTipoItem_atributo"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_campofile_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campofile"
    ADD CONSTRAINT "administrarItems_campofile_item_id_fkey" FOREIGN KEY (item_id) REFERENCES "administrarItems_itembase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_campoimagen_atributo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campoimagen"
    ADD CONSTRAINT "administrarItems_campoimagen_atributo_id_fkey" FOREIGN KEY (atributo_id) REFERENCES "administrarTipoItem_atributo"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_campoimagen_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campoimagen"
    ADD CONSTRAINT "administrarItems_campoimagen_item_id_fkey" FOREIGN KEY (item_id) REFERENCES "administrarItems_itembase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_camponumero_atributo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_camponumero"
    ADD CONSTRAINT "administrarItems_camponumero_atributo_id_fkey" FOREIGN KEY (atributo_id) REFERENCES "administrarTipoItem_atributo"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_camponumero_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_camponumero"
    ADD CONSTRAINT "administrarItems_camponumero_item_id_fkey" FOREIGN KEY (item_id) REFERENCES "administrarItems_itembase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_campotextocorto_atributo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campotextocorto"
    ADD CONSTRAINT "administrarItems_campotextocorto_atributo_id_fkey" FOREIGN KEY (atributo_id) REFERENCES "administrarTipoItem_atributo"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_campotextocorto_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campotextocorto"
    ADD CONSTRAINT "administrarItems_campotextocorto_item_id_fkey" FOREIGN KEY (item_id) REFERENCES "administrarItems_itembase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_campotextolargo_atributo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campotextolargo"
    ADD CONSTRAINT "administrarItems_campotextolargo_atributo_id_fkey" FOREIGN KEY (atributo_id) REFERENCES "administrarTipoItem_atributo"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_campotextolargo_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_campotextolargo"
    ADD CONSTRAINT "administrarItems_campotextolargo_item_id_fkey" FOREIGN KEY (item_id) REFERENCES "administrarItems_itembase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_itembase_tipoitem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_itembase"
    ADD CONSTRAINT "administrarItems_itembase_tipoitem_id_fkey" FOREIGN KEY (tipoitem_id) REFERENCES "administrarTipoItem_tipoitem"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_itembase_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_itembase"
    ADD CONSTRAINT "administrarItems_itembase_usuario_id_fkey" FOREIGN KEY (usuario_id) REFERENCES autenticacion_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_itembase_usuario_modificacion_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_itembase"
    ADD CONSTRAINT "administrarItems_itembase_usuario_modificacion_id_fkey" FOREIGN KEY (usuario_modificacion_id) REFERENCES autenticacion_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_itemrelacion_itemHijo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_itemrelacion"
    ADD CONSTRAINT "administrarItems_itemrelacion_itemHijo_id_fkey" FOREIGN KEY ("itemHijo_id") REFERENCES "administrarItems_itembase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarItems_itemrelacion_itemPadre_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_itemrelacion"
    ADD CONSTRAINT "administrarItems_itemrelacion_itemPadre_id_fkey" FOREIGN KEY ("itemPadre_id") REFERENCES "administrarItems_itembase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarLineaBase_lineabase_fase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarLineaBase_lineabase"
    ADD CONSTRAINT "administrarLineaBase_lineabase_fase_id_fkey" FOREIGN KEY (fase_id) REFERENCES "administrarFases_fase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarLineaBase_solicitudcambios_fase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarLineaBase_solicitudcambios"
    ADD CONSTRAINT "administrarLineaBase_solicitudcambios_fase_id_fkey" FOREIGN KEY (fase_id) REFERENCES "administrarFases_fase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarLineaBase_solicitudcambios_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarLineaBase_solicitudcambios"
    ADD CONSTRAINT "administrarLineaBase_solicitudcambios_usuario_id_fkey" FOREIGN KEY (usuario_id) REFERENCES autenticacion_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarLineaBase_votacion_solicitud_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarLineaBase_votacion"
    ADD CONSTRAINT "administrarLineaBase_votacion_solicitud_id_fkey" FOREIGN KEY (solicitud_id) REFERENCES "administrarLineaBase_solicitudcambios"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarLineaBase_votacion_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarLineaBase_votacion"
    ADD CONSTRAINT "administrarLineaBase_votacion_usuario_id_fkey" FOREIGN KEY (usuario_id) REFERENCES autenticacion_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarProyectos_proyecto_lider_proyecto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarProyectos_proyecto"
    ADD CONSTRAINT "administrarProyectos_proyecto_lider_proyecto_id_fkey" FOREIGN KEY (lider_proyecto_id) REFERENCES autenticacion_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarProyectos_usuariosvinculadospro_cod_proyecto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarProyectos_usuariosvinculadosproyectos"
    ADD CONSTRAINT "administrarProyectos_usuariosvinculadospro_cod_proyecto_id_fkey" FOREIGN KEY (cod_proyecto_id) REFERENCES "administrarProyectos_proyecto"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarProyectos_usuariosvinculadosproy_cod_usuario_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarProyectos_usuariosvinculadosproyectos"
    ADD CONSTRAINT "administrarProyectos_usuariosvinculadosproy_cod_usuario_id_fkey" FOREIGN KEY (cod_usuario_id) REFERENCES autenticacion_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarRolesPermisos_rol_grupo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarRolesPermisos_rol"
    ADD CONSTRAINT "administrarRolesPermisos_rol_grupo_id_fkey" FOREIGN KEY (grupo_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarRolesPermisos_rol_proyecto_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarRolesPermisos_rol"
    ADD CONSTRAINT "administrarRolesPermisos_rol_proyecto_id_fkey" FOREIGN KEY (proyecto_id) REFERENCES "administrarProyectos_proyecto"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarTipoItem_atributo_tipoDeItem_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarTipoItem_atributo"
    ADD CONSTRAINT "administrarTipoItem_atributo_tipoDeItem_id_fkey" FOREIGN KEY ("tipoDeItem_id") REFERENCES "administrarTipoItem_tipoitem"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: administrarTipoItem_tipoitem_fase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarTipoItem_tipoitem"
    ADD CONSTRAINT "administrarTipoItem_tipoitem_fase_id_fkey" FOREIGN KEY (fase_id) REFERENCES "administrarFases_fase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: autenticacion_usuario_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY autenticacion_usuario_groups
    ADD CONSTRAINT autenticacion_usuario_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: autenticacion_usuario_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY autenticacion_usuario_user_permissions
    ADD CONSTRAINT autenticacion_usuario_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_d043b34a; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_d043b34a FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_f4b32aac; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT group_id_refs_id_f4b32aac FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guardian_groupobjectpermission_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY guardian_groupobjectpermission
    ADD CONSTRAINT guardian_groupobjectpermission_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guardian_groupobjectpermission_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY guardian_groupobjectpermission
    ADD CONSTRAINT guardian_groupobjectpermission_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guardian_groupobjectpermission_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY guardian_groupobjectpermission
    ADD CONSTRAINT guardian_groupobjectpermission_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guardian_userobjectpermission_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY guardian_userobjectpermission
    ADD CONSTRAINT guardian_userobjectpermission_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guardian_userobjectpermission_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY guardian_userobjectpermission
    ADD CONSTRAINT guardian_userobjectpermission_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: guardian_userobjectpermission_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY guardian_userobjectpermission
    ADD CONSTRAINT guardian_userobjectpermission_user_id_fkey FOREIGN KEY (user_id) REFERENCES autenticacion_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: itembase_id_refs_id_16f0d151; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_itembase_solicitudes"
    ADD CONSTRAINT itembase_id_refs_id_16f0d151 FOREIGN KEY (itembase_id) REFERENCES "administrarItems_itembase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: linea_base_id_refs_id_be977500; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_itembase"
    ADD CONSTRAINT linea_base_id_refs_id_be977500 FOREIGN KEY (linea_base_id) REFERENCES "administrarLineaBase_lineabase"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reversion_version_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY reversion_version
    ADD CONSTRAINT reversion_version_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: reversion_version_revision_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY reversion_version
    ADD CONSTRAINT reversion_version_revision_id_fkey FOREIGN KEY (revision_id) REFERENCES reversion_revision(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: solicitudcambios_id_refs_id_5b77e6bd; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarItems_itembase_solicitudes"
    ADD CONSTRAINT solicitudcambios_id_refs_id_5b77e6bd FOREIGN KEY (solicitudcambios_id) REFERENCES "administrarLineaBase_solicitudcambios"(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_89940856; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY reversion_revision
    ADD CONSTRAINT user_id_refs_id_89940856 FOREIGN KEY (user_id) REFERENCES autenticacion_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_febc855e; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT user_id_refs_id_febc855e FOREIGN KEY (user_id) REFERENCES autenticacion_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: usuario_id_refs_id_0ce0f49c; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY autenticacion_usuario_groups
    ADD CONSTRAINT usuario_id_refs_id_0ce0f49c FOREIGN KEY (usuario_id) REFERENCES autenticacion_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: usuario_id_refs_id_6826e484; Type: FK CONSTRAINT; Schema: public; Owner: zar
--

ALTER TABLE ONLY autenticacion_usuario_user_permissions
    ADD CONSTRAINT usuario_id_refs_id_6826e484 FOREIGN KEY (usuario_id) REFERENCES autenticacion_usuario(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

