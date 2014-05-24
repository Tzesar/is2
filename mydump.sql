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
-- Name: administrarItems_itemrelacion; Type: TABLE; Schema: public; Owner: zar; Tablespace: 
--

CREATE TABLE "administrarItems_itemrelacion" (
    id integer NOT NULL,
    "itemPadre_id" integer NOT NULL,
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

ALTER TABLE ONLY "administrarItems_itemrelacion" ALTER COLUMN id SET DEFAULT nextval('"administrarItems_itemrelacion_id_seq"'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: zar
--

ALTER TABLE ONLY "administrarLineaBase_lineabase" ALTER COLUMN id SET DEFAULT nextval('"administrarLineaBase_lineabase_id_seq"'::regclass);


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
\.


--
-- Name: administrarFases_fase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarFases_fase_id_seq"', 1, false);


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
\.


--
-- Name: administrarItems_camponumero_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_camponumero_id_seq"', 1, false);


--
-- Data for Name: administrarItems_campotextocorto; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_campotextocorto" (id, item_id, atributo_id, valor) FROM stdin;
\.


--
-- Name: administrarItems_campotextocorto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_campotextocorto_id_seq"', 1, false);


--
-- Data for Name: administrarItems_campotextolargo; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_campotextolargo" (id, item_id, atributo_id, valor) FROM stdin;
\.


--
-- Name: administrarItems_campotextolargo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_campotextolargo_id_seq"', 1, false);


--
-- Data for Name: administrarItems_itembase; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_itembase" (id, usuario_id, usuario_modificacion_id, nombre, descripcion, estado, fecha_creacion, fecha_modificacion, tipoitem_id, complejidad, costo, tiempo, version, linea_base_id) FROM stdin;
\.


--
-- Name: administrarItems_itembase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_itembase_id_seq"', 1, false);


--
-- Data for Name: administrarItems_itemrelacion; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarItems_itemrelacion" (id, "itemPadre_id", "itemHijo_id", estado) FROM stdin;
\.


--
-- Name: administrarItems_itemrelacion_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarItems_itemrelacion_id_seq"', 1, false);


--
-- Data for Name: administrarLineaBase_lineabase; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarLineaBase_lineabase" (id, fase_id, fecha_creacion, fecha_modificacion, observaciones) FROM stdin;
\.


--
-- Name: administrarLineaBase_lineabase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarLineaBase_lineabase_id_seq"', 1, false);


--
-- Data for Name: administrarProyectos_proyecto; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarProyectos_proyecto" (id, nombre, lider_proyecto_id, descripcion, fecha_creacion, fecha_inicio, fecha_fin, estado, observaciones) FROM stdin;
\.


--
-- Name: administrarProyectos_proyecto_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarProyectos_proyecto_id_seq"', 1, false);


--
-- Data for Name: administrarProyectos_usuariosvinculadosproyectos; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarProyectos_usuariosvinculadosproyectos" (id, cod_proyecto_id, cod_usuario_id, habilitado) FROM stdin;
\.


--
-- Name: administrarProyectos_usuariosvinculadosproyectos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarProyectos_usuariosvinculadosproyectos_id_seq"', 1, false);


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
\.


--
-- Name: administrarRolesPermisos_rol_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarRolesPermisos_rol_id_seq"', 1, false);


--
-- Data for Name: administrarTipoItem_atributo; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarTipoItem_atributo" (id, nombre, tipo, "tipoDeItem_id", descripcion) FROM stdin;
\.


--
-- Name: administrarTipoItem_atributo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarTipoItem_atributo_id_seq"', 1, false);


--
-- Data for Name: administrarTipoItem_tipoitem; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY "administrarTipoItem_tipoitem" (id, nombre, fase_id, descripcion) FROM stdin;
\.


--
-- Name: administrarTipoItem_tipoitem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('"administrarTipoItem_tipoitem_id_seq"', 1, false);


--
-- Data for Name: autenticacion_usuario; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY autenticacion_usuario (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, telefono) FROM stdin;
1	pbkdf2_sha256$12000$ISatbLE5CkTw$v7W16fqVWTUtzFaWjMHKeuDvFNx6hPBCDMJWSoIzxlg=	2014-05-21 11:20:55.138744-04	t	admin			admin@zarpm.org	t	t	2014-05-21 11:20:55.138744-04	
-1		2014-05-21 11:20:55.528227-04	f	AnonymousUser				f	t	2014-05-21 11:20:55.528291-04	
\.


--
-- Data for Name: autenticacion_usuario_groups; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY autenticacion_usuario_groups (id, usuario_id, group_id) FROM stdin;
\.


--
-- Name: autenticacion_usuario_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('autenticacion_usuario_groups_id_seq', 1, false);


--
-- Name: autenticacion_usuario_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('autenticacion_usuario_id_seq', 1, true);


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
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


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
44	Puede crear permiso	12	crear_permiso
45	Puede modificar permiso	12	modificar_permiso
46	Puede borrar permiso	12	borrar_permiso
47	Puede crear rol	13	crear_rol
48	Puede modificar rol	13	modificar_rol
49	Puede borrar rol	13	borrar_rol
50	Puede crear TipoItem	14	crear_tipoitem
51	Puede modificar TipoItem	14	modificar_tipoitem
52	Puede borrar TipoItem	14	borrar_tipoitem
53	Puede crear Atributo	15	crear_atributo
54	Puede modificar Atributo	15	modificar_atributo
55	Puede borrar Atributo	15	borrar_atributo
56	Puede crear item base	16	crear_itembase
57	Puede modificar item base	16	modificar_itembase
58	Puede borrar item base	16	borrar_itembase
59	Puede crear item relacion	17	crear_itemrelacion
60	Puede modificar item relacion	17	modificar_itemrelacion
61	Puede borrar item relacion	17	borrar_itemrelacion
62	Puede crear campo numero	18	crear_camponumero
63	Puede modificar campo numero	18	modificar_camponumero
64	Puede borrar campo numero	18	borrar_camponumero
65	Puede crear campo texto corto	19	crear_campotextocorto
66	Puede modificar campo texto corto	19	modificar_campotextocorto
67	Puede borrar campo texto corto	19	borrar_campotextocorto
68	Puede crear campo texto largo	20	crear_campotextolargo
69	Puede modificar campo texto largo	20	modificar_campotextolargo
70	Puede borrar campo texto largo	20	borrar_campotextolargo
71	Puede crear campo file	21	crear_campofile
72	Puede modificar campo file	21	modificar_campofile
73	Puede borrar campo file	21	borrar_campofile
74	Puede crear campo imagen	22	crear_campoimagen
75	Puede modificar campo imagen	22	modificar_campoimagen
76	Puede borrar campo imagen	22	borrar_campoimagen
77	Puede crear linea base	23	crear_lineabase
78	Puede modificar linea base	23	modificar_lineabase
79	Puede borrar linea base	23	borrar_lineabase
80	Puede crear user object permission	24	crear_userobjectpermission
81	Puede modificar user object permission	24	modificar_userobjectpermission
82	Puede borrar user object permission	24	borrar_userobjectpermission
83	Puede crear group object permission	25	crear_groupobjectpermission
84	Puede modificar group object permission	25	modificar_groupobjectpermission
85	Puede borrar group object permission	25	borrar_groupobjectpermission
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('auth_permission_id_seq', 85, true);


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
24	user object permission	guardian	userobjectpermission
25	group object permission	guardian	groupobjectpermission
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('django_content_type_id_seq', 25, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: guardian_groupobjectpermission; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY guardian_groupobjectpermission (id, permission_id, content_type_id, object_pk, group_id) FROM stdin;
\.


--
-- Name: guardian_groupobjectpermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('guardian_groupobjectpermission_id_seq', 1, false);


--
-- Data for Name: guardian_userobjectpermission; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY guardian_userobjectpermission (id, permission_id, content_type_id, object_pk, user_id) FROM stdin;
\.


--
-- Name: guardian_userobjectpermission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('guardian_userobjectpermission_id_seq', 1, false);


--
-- Data for Name: reversion_revision; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY reversion_revision (id, manager_slug, date_created, user_id, comment) FROM stdin;
\.


--
-- Name: reversion_revision_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('reversion_revision_id_seq', 1, false);


--
-- Data for Name: reversion_version; Type: TABLE DATA; Schema: public; Owner: zar
--

COPY reversion_version (id, revision_id, object_id, object_id_int, content_type_id, format, serialized_data, object_repr) FROM stdin;
\.


--
-- Name: reversion_version_id_seq; Type: SEQUENCE SET; Schema: public; Owner: zar
--

SELECT pg_catalog.setval('reversion_version_id_seq', 1, false);


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

